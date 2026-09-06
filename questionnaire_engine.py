"""
Questionnaire engine for INAI.

Drives the state machine:
  main question -> patient answer -> Gemini interpretation -> YES/NO/UNKNOWN
  -> follow-up questions when needed -> next main question -> completion -> risk

Session position is tracked with two integers stored on ScreeningSession:
  current_index           - index into questions.QUESTIONS (which main question)
  current_followup_index  - -1 while on the main question itself, otherwise the
                             index into that question's follow_ups list

This keeps "current question" always unambiguous and easy to resume across
separate HTTP requests (each Twilio webhook call, or each /analyze call, is a
separate request - the DB row is the only thing that remembers where we are).
"""

from datetime import datetime

import ai_service
import risk_engine
from questions import QUESTIONS
from models import ScreeningSession, ScreeningAnswer


def create_session(db, patient_id):
    session = ScreeningSession(patient_id=patient_id, current_index=0, current_followup_index=-1)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_session(db, session_id):
    return db.query(ScreeningSession).filter(ScreeningSession.id == session_id).first()


def _main_question(session):
    if session.current_index >= len(QUESTIONS):
        return None
    return QUESTIONS[session.current_index]


def get_current_question(session):
    """Returns the question dict the patient should be asked right now, or None if
    the screening is already complete."""
    main_q = _main_question(session)
    if main_q is None:
        return None

    if session.current_followup_index == -1:
        return main_q

    follow_ups = main_q.get("follow_ups", [])
    if session.current_followup_index < len(follow_ups):
        return follow_ups[session.current_followup_index]

    # Shouldn't normally happen, but guard defensively.
    return main_q


def _advance_position(session, interpreted_answer):
    """Move current_index / current_followup_index forward based on how the
    question that was just answered turned out."""
    main_q = _main_question(session)
    if main_q is None:
        return

    if session.current_followup_index == -1:
        # We just answered a MAIN question.
        follow_ups = main_q.get("follow_ups", [])
        if interpreted_answer == "YES" and follow_ups:
            session.current_followup_index = 0
            return
        # No follow-ups needed - move to the next main question.
        session.current_index += 1
        session.current_followup_index = -1
        return

    # We just answered a FOLLOW-UP question.
    follow_ups = main_q.get("follow_ups", [])
    next_followup_index = session.current_followup_index + 1
    if next_followup_index < len(follow_ups):
        session.current_followup_index = next_followup_index
        return

    # No more follow-ups for this main question - move on.
    session.current_index += 1
    session.current_followup_index = -1


def submit_answer(db, session, raw_answer_text, language="en"):
    """
    Records the patient's answer to the current question, interprets it via
    ai_service, advances the session's position, and completes the screening
    (computing risk) if there are no more questions left.

    Returns a dict:
    {
        "interpretation": {"interpreted_answer": ..., "detected_symptoms": [...]},
        "status": "in_progress" | "completed",
        "next_question": <question dict> | None,
        "risk_level": str | None,
        "guidance": str | None,
    }
    """
    current_q = get_current_question(session)
    if current_q is None:
        # Nothing left to answer - already completed.
        return {
            "interpretation": None,
            "status": "completed",
            "next_question": None,
            "risk_level": session.risk_level,
            "guidance": session.guidance,
        }

    result = ai_service.interpret_answer(current_q, raw_answer_text, language=language)

    answer_row = ScreeningAnswer(
        session_id=session.id,
        question_id=current_q["id"],
        question_text=current_q.get("text", {}).get(language)
        or current_q.get("text", {}).get("en", ""),
        category=current_q.get("category"),
        patient_answer_raw=raw_answer_text,
        interpreted_answer=result["interpreted_answer"],
        detected_symptoms=",".join(result["detected_symptoms"]),
    )
    db.add(answer_row)

    for cat in result["detected_symptoms"]:
        session.add_flagged_category(cat)

    _advance_position(session, result["interpreted_answer"])

    next_q = get_current_question(session)

    if next_q is None:
        risk_level, guidance = risk_engine.compute_risk(session.get_flagged_categories())
        session.status = "completed"
        session.risk_level = risk_level
        session.guidance = guidance
        session.completed_at = datetime.utcnow()

    db.commit()
    db.refresh(session)

    return {
        "interpretation": {
            "interpreted_answer": result["interpreted_answer"],
            "detected_symptoms": result["detected_symptoms"],
        },
        "status": session.status,
        "next_question": next_q,
        "risk_level": session.risk_level if session.status == "completed" else None,
        "guidance": session.guidance if session.status == "completed" else None,
    }
