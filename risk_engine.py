"""
Risk engine for the INAI hackathon prototype.

Takes the set of symptom categories flagged as YES during a screening and
produces a LOW / MODERATE / HIGH risk level plus a plain-language guidance
message. This is a simple prototype scoring system, not clinically
validated, and is never presented to the patient as a diagnosis.
"""

from risk_rules import (
    EMERGENCY_CATEGORIES,
    MODERATE_WEIGHT_CATEGORIES,
    LOW_WEIGHT_CATEGORIES,
    MODERATE_RISK_THRESHOLD,
)

HIGH_RISK_GUIDANCE = (
    "Some of your answers point to symptoms that can be serious during pregnancy. "
    "Please contact a qualified healthcare professional or your nearest healthcare "
    "facility as soon as possible. This screening is not a diagnosis."
)

MODERATE_RISK_GUIDANCE = (
    "Your answers suggest some symptoms worth getting checked. Please plan to "
    "contact a qualified healthcare professional or visit your nearest healthcare "
    "facility soon. This screening is not a diagnosis."
)

LOW_RISK_GUIDANCE = (
    "Your answers do not show signs of an urgent problem right now. Please continue "
    "your regular prenatal checkups, and contact a qualified healthcare professional "
    "if anything changes or you feel worried. This screening is not a diagnosis."
)


def compute_risk(flagged_categories):
    """
    flagged_categories: iterable of category strings that were answered YES
    during the screening (main questions and/or follow-ups).

    Returns: (risk_level: str, guidance: str)
    """
    categories = set(flagged_categories or [])

    if categories & EMERGENCY_CATEGORIES:
        return "HIGH", HIGH_RISK_GUIDANCE

    score = 0
    for cat in categories:
        score += MODERATE_WEIGHT_CATEGORIES.get(cat, 0)
        score += LOW_WEIGHT_CATEGORIES.get(cat, 0)

    if score >= MODERATE_RISK_THRESHOLD:
        return "MODERATE", MODERATE_RISK_GUIDANCE

    if score > 0:
        return "LOW", LOW_RISK_GUIDANCE

    return "LOW", LOW_RISK_GUIDANCE
