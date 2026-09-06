"""
INAI backend - FastAPI application.

Run locally with:
    uvicorn main:app --reload

Then expose it publicly for Twilio with:
    ngrok http 8000

See README.md for full setup instructions (env vars, Twilio webhook config, etc.)
"""

import os
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Depends, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
from twilio.twiml.voice_response import VoiceResponse, Gather

import ai_service
import history_service
import questionnaire_engine
from database import init_db, get_db
from models import ScreeningSession
from questions import get_question_text

app = FastAPI(title="INAI Maternal Healthcare Screening API")

# Allow the Vite dev server (and any configured frontend origin) to call the API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hackathon prototype - tighten this for production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    # Creates inai.db and all tables automatically if they don't already exist.
    init_db()


@app.get("/")
def root():
    return {
        "service": "INAI Maternal Healthcare Screening API",
        "status": "ok",
        "gemini_configured": ai_service.is_gemini_configured(),
        "disclaimer": (
            "This is a hackathon prototype. Risk levels are produced by an "
            "unvalidated rule-based scoring system and are not a medical diagnosis."
        ),
    }


# --------------------------------------------------------------------------
# Twilio Voice webhooks
# --------------------------------------------------------------------------

DEFAULT_VOICE_LANGUAGE = os.getenv("VOICE_LANGUAGE", "en-IN")


def _twiml_response(twiml: VoiceResponse) -> Response:
    return Response(content=str(twiml), media_type="application/xml")


def _ask_question_twiml(question_text: str) -> VoiceResponse:
    twiml = VoiceResponse()
    gather = Gather(
        input="speech",
        action="/process-speech",
        method="POST",
        speech_timeout="auto",
        language=DEFAULT_VOICE_LANGUAGE,
    )
    gather.say(question_text)
    twiml.append(gather)
    # If Twilio doesn't receive speech input at all, repeat the question once.
    twiml.redirect("/incoming-call")
    return twiml


@app.post("/incoming-call")
async def incoming_call(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    call_sid = form.get("CallSid", "")
    from_number = form.get("From", "unknown")

    if not call_sid:
        twiml = VoiceResponse()
        twiml.say("Sorry, something went wrong. Please try calling again.")
        return _twiml_response(twiml)

    session = db.query(ScreeningSession).filter(ScreeningSession.id == call_sid).first()
    if session is None:
        session = ScreeningSession(
            id=call_sid,
            patient_id=from_number,
            current_index=0,
            current_followup_index=-1,
        )
        db.add(session)
        db.commit()
        db.refresh(session)

    question = questionnaire_engine.get_current_question(session)
    if question is None:
        twiml = VoiceResponse()
        twiml.say(session.guidance or "Thank you. Your screening is already complete.")
        return _twiml_response(twiml)

    question_text = get_question_text(question, "en")
    twiml = _ask_question_twiml(question_text)
    return _twiml_response(twiml)


@app.post("/process-speech")
async def process_speech(request: Request, db: Session = Depends(get_db)):
    form = await request.form()
    call_sid = form.get("CallSid", "")
    speech_result = form.get("SpeechResult", "")

    session = db.query(ScreeningSession).filter(ScreeningSession.id == call_sid).first()
    if session is None:
        twiml = VoiceResponse()
        twiml.say("Sorry, we could not find your screening session. Please call again.")
        return _twiml_response(twiml)

    if not speech_result:
        # No speech detected - re-ask the current question rather than guessing.
        question = questionnaire_engine.get_current_question(session)
        question_text = get_question_text(question, "en") if question else (
            session.guidance or "Thank you."
        )
        twiml = _ask_question_twiml(question_text) if question else VoiceResponse()
        if not question:
            twiml.say(question_text)
        return _twiml_response(twiml)

    result = questionnaire_engine.submit_answer(db, session, speech_result, language="en")

    twiml = VoiceResponse()
    if result["status"] == "completed":
        twiml.say(result["guidance"])
        twiml.say(
            "This screening result is not a medical diagnosis. "
            "Please contact a qualified healthcare professional for any concerns."
        )
        return _twiml_response(twiml)

    next_question_text = get_question_text(result["next_question"], "en")
    twiml = _ask_question_twiml(next_question_text)
    return _twiml_response(twiml)


# --------------------------------------------------------------------------
# Text-based screening (no phone call needed) - useful for demos/testing
# --------------------------------------------------------------------------

class AnalyzeRequest(BaseModel):
    patient_id: Optional[str] = None
    session_id: Optional[str] = None
    answer_text: Optional[str] = None
    language: Optional[str] = "en"


@app.post("/analyze")
def analyze(payload: AnalyzeRequest, db: Session = Depends(get_db)):
    language = payload.language or "en"

    if payload.session_id:
        session = questionnaire_engine.get_session(db, payload.session_id)
        if session is None:
            raise HTTPException(status_code=404, detail="session_id not found")
    else:
        patient_id = payload.patient_id or f"WEB-{datetime.utcnow().timestamp():.0f}"
        session = questionnaire_engine.create_session(db, patient_id)

    if payload.answer_text is None:
        # First call for this session: just return the current question.
        question = questionnaire_engine.get_current_question(session)
        return {
            "session_id": session.id,
            "patient_id": session.patient_id,
            "status": session.status,
            "question": _question_payload(question, language),
            "interpretation": None,
            "risk_level": session.risk_level,
            "guidance": session.guidance,
        }

    result = questionnaire_engine.submit_answer(
        db, session, payload.answer_text, language=language
    )

    return {
        "session_id": session.id,
        "patient_id": session.patient_id,
        "status": result["status"],
        "question": _question_payload(result["next_question"], language),
        "interpretation": result["interpretation"],
        "risk_level": result["risk_level"],
        "guidance": result["guidance"],
    }


def _question_payload(question, language):
    if question is None:
        return None
    return {"id": question["id"], "text": get_question_text(question, language)}


# --------------------------------------------------------------------------
# History endpoints (used by the frontend dashboard)
# --------------------------------------------------------------------------

@app.get("/history")
def get_all_history(db: Session = Depends(get_db)):
    return history_service.list_all_history(db)


@app.get("/history/{patient_id}")
def get_patient_history(patient_id: str, db: Session = Depends(get_db)):
    return history_service.list_patient_history(db, patient_id)


@app.get("/history/{patient_id}/{screening_id}")
def get_screening_detail(patient_id: str, screening_id: str, db: Session = Depends(get_db)):
    detail = history_service.get_screening_detail(db, patient_id, screening_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="Screening not found")
    return detail


class ReviewRequest(BaseModel):
    reviewed: Optional[bool] = True


@app.patch("/history/{patient_id}/{screening_id}/review")
def review_screening(
    patient_id: str,
    screening_id: str,
    payload: ReviewRequest,
    db: Session = Depends(get_db),
):
    updated = history_service.mark_reviewed(
        db, patient_id, screening_id, reviewed=payload.reviewed
    )
    if updated is None:
        raise HTTPException(status_code=404, detail="Screening not found")
    return updated
