"""
SQLAlchemy models for INAI.

ScreeningSession - one screening attempt (one phone call, or one /analyze
                   text-demo run) for a patient/session id.
ScreeningAnswer  - one question asked + how it was answered, tied to a session.
"""

import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Integer,
    Boolean,
    DateTime,
    ForeignKey,
    Text,
)
from sqlalchemy.orm import relationship

from database import Base


def new_id():
    return str(uuid.uuid4())


class ScreeningSession(Base):
    __tablename__ = "screening_sessions"

    id = Column(String, primary_key=True, default=new_id)  # screening_id
    patient_id = Column(String, index=True, nullable=False)

    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # Position in the QUESTIONS list (index into questions.QUESTIONS)
    current_index = Column(Integer, default=0)
    # -1 means "on the main question at current_index"; >=0 means
    # "on follow-up number N of the question at current_index"
    current_followup_index = Column(Integer, default=-1)

    status = Column(String, default="in_progress")  # in_progress | completed
    risk_level = Column(String, nullable=True)  # LOW | MODERATE | HIGH
    guidance = Column(Text, nullable=True)

    reviewed = Column(Boolean, default=False)

    # Comma-separated list of flagged symptom categories (kept simple for SQLite)
    flagged_categories = Column(Text, default="")

    answers = relationship(
        "ScreeningAnswer", back_populates="session", cascade="all, delete-orphan"
    )

    def get_flagged_categories(self):
        return [c for c in (self.flagged_categories or "").split(",") if c]

    def add_flagged_category(self, category):
        cats = set(self.get_flagged_categories())
        cats.add(category)
        self.flagged_categories = ",".join(sorted(cats))


class ScreeningAnswer(Base):
    __tablename__ = "screening_answers"

    id = Column(String, primary_key=True, default=new_id)
    session_id = Column(String, ForeignKey("screening_sessions.id"), nullable=False)

    question_id = Column(String, nullable=False)
    question_text = Column(Text, nullable=False)
    category = Column(String, nullable=True)

    patient_answer_raw = Column(Text, nullable=False)
    interpreted_answer = Column(String, nullable=False)  # YES | NO | UNKNOWN

    # Comma-separated detected symptom categories for this specific answer
    detected_symptoms = Column(Text, default="")

    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ScreeningSession", back_populates="answers")

    def get_detected_symptoms(self):
        return [c for c in (self.detected_symptoms or "").split(",") if c]
