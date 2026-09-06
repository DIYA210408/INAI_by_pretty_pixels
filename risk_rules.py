"""
Risk scoring rules for the INAI hackathon prototype.

IMPORTANT: These rules are a simple, NOT clinically validated prototype
scoring system built for a 24-hour hackathon. They must never be presented
as a medical diagnosis or a medically validated prediction. Always pair a
HIGH/MODERATE result with guidance to contact a qualified healthcare
professional or facility.

Categories correspond to the `category` field on questions in questions.py.
"""

# Categories that, if flagged (YES), are treated as potential emergencies
# and immediately push the screening to HIGH risk regardless of anything else.
EMERGENCY_CATEGORIES = {
    "bleeding",
    "seizure",
    "abdominal_pain",
    "vision",
    "breathlessness",
}

# Categories that contribute a moderate amount of risk score each time they
# are flagged, without being an automatic emergency on their own.
MODERATE_WEIGHT_CATEGORIES = {
    "headache": 2,
    "fetal_movement": 2,
    "contractions": 2,
    "vomiting": 1,
    "fever": 1,
    "swelling": 1,
    "fluid_leak": 2,
    "dizziness": 1,
    "back_pain": 1,
}

# Categories that contribute a small amount of risk score - generally
# lower-urgency wellbeing/history items.
LOW_WEIGHT_CATEGORIES = {
    "urinary": 1,
    "appetite": 1,
    "sleep": 1,
    "mental_health": 1,
    "history": 1,
    "general_wellbeing": 1,
}

# Score thresholds used by risk_engine.py to translate an accumulated
# moderate/low score into a MODERATE vs LOW final result (when no emergency
# category was triggered).
MODERATE_RISK_THRESHOLD = 3
