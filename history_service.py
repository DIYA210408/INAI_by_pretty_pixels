"""
History service for INAI.

Provides the read/update queries backing the /history endpoints: listing
screenings (all, or per patient), fetching one screening's full transcript,
and marking a screening as reviewed by a healthcare worker.
"""

from models import ScreeningSession


def _summary(session):
    return {
        "screening_id": session.id,
        "patient_id": session.patient_id,
        "started_at": session.started_at.isoformat() if session.started_at else None,
        "completed_at": session.completed_at.isoformat() if session.completed_at else None,
        "status": session.status,
        "risk_level": session.risk_level,
        "detected_symptoms": session.get_flagged_categories(),
        "ai_summary": _build_ai_summary(session),
        "reviewed": session.reviewed,
    }


def _build_ai_summary(session):
    categories = session.get_flagged_categories()
    if not categories:
        if session.status == "completed":
            return "No concerning symptoms were flagged during this screening."
        return "Screening in progress - no symptoms flagged yet."

    readable = ", ".join(c.replace("_", " ") for c in categories)
    return f"Patient flagged the following during screening: {readable}."


def list_all_history(db):
    sessions = (
        db.query(ScreeningSession)
        .order_by(ScreeningSession.started_at.desc())
        .all()
    )
    return [_summary(s) for s in sessions]


def list_patient_history(db, patient_id):
    sessions = (
        db.query(ScreeningSession)
        .filter(ScreeningSession.patient_id == patient_id)
        .order_by(ScreeningSession.started_at.desc())
        .all()
    )
    return [_summary(s) for s in sessions]


def get_screening_detail(db, patient_id, screening_id):
    session = (
        db.query(ScreeningSession)
        .filter(
            ScreeningSession.id == screening_id,
            ScreeningSession.patient_id == patient_id,
        )
        .first()
    )
    if session is None:
        return None

    detail = _summary(session)
    detail["answers"] = [
        {
            "question_id": a.question_id,
            "question_text": a.question_text,
            "category": a.category,
            "patient_answer_raw": a.patient_answer_raw,
            "interpreted_answer": a.interpreted_answer,
            "detected_symptoms": a.get_detected_symptoms(),
            "created_at": a.created_at.isoformat() if a.created_at else None,
        }
        for a in session.answers
    ]
    return detail


def mark_reviewed(db, patient_id, screening_id, reviewed=True):
    session = (
        db.query(ScreeningSession)
        .filter(
            ScreeningSession.id == screening_id,
            ScreeningSession.patient_id == patient_id,
        )
        .first()
    )
    if session is None:
        return None

    session.reviewed = reviewed
    db.commit()
    db.refresh(session)
    return _summary(session)
