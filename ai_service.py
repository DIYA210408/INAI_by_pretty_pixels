"""
AI interpretation service for INAI.

Uses Google Gemini (current google-genai Python SDK) to interpret a patient's
free-form spoken answer (English / Tamil / Tanglish) into a structured
YES / NO / UNKNOWN result, plus any explicitly-mentioned extra symptoms.

Hard safety rules (enforced via the system prompt AND via post-processing):
  - Never diagnose a disease.
  - Never prescribe medicine.
  - Never claim to replace a doctor.
  - Never invent symptoms the patient did not describe.
  - If unclear, return UNKNOWN rather than guessing.

If GEMINI_API_KEY is not configured, this module falls back to a simple
keyword-based interpreter so the rest of the system (questionnaire engine,
risk engine, endpoints) can still be exercised and tested locally without
external credentials. This fallback is intentionally conservative and is
NOT a substitute for the Gemini interpretation.
"""

import os
import json
import re

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

_client = None
_gemini_available = False

if GEMINI_API_KEY:
    try:
        from google import genai

        _client = genai.Client(api_key=GEMINI_API_KEY)
        _gemini_available = True
    except Exception:
        # SDK not installed or client failed to initialize - fall back safely.
        _client = None
        _gemini_available = False


SYSTEM_INSTRUCTIONS = """You are a careful multilingual (English, Tamil, Tanglish) assistant \
helping interpret a pregnant patient's spoken answer to a maternal health screening question.

Your ONLY job is to classify the patient's answer to the given question as YES, NO, or UNKNOWN, \
and list any symptoms the patient explicitly mentioned.

Rules you MUST follow:
- Do NOT diagnose any disease or condition.
- Do NOT prescribe or suggest any medicine or treatment.
- Do NOT claim to replace a doctor or medical professional.
- Do NOT invent or assume symptoms the patient did not mention.
- If the answer is ambiguous, unclear, or you are not confident, respond with UNKNOWN. \
Never guess YES or NO when unsure.
- Understand meaning, not just exact keywords - the patient may answer in English, Tamil, \
or Tanglish (Tamil written in English letters), and may phrase things indirectly.

Respond ONLY with a single JSON object, no other text, no markdown fences, in exactly this shape:
{"interpreted_answer": "YES" | "NO" | "UNKNOWN", "mentioned_symptoms": [<short strings, empty list if none>]}
"""


def _build_prompt(question_text, patient_answer):
    return (
        f"{SYSTEM_INSTRUCTIONS}\n\n"
        f"Question asked: {question_text}\n"
        f"Patient's spoken answer: {patient_answer}\n"
    )


def _call_gemini(question_text, patient_answer):
    prompt = _build_prompt(question_text, patient_answer)
    response = _client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )
    text = (response.text or "").strip()
    # Strip accidental markdown fences just in case.
    text = re.sub(r"^```(json)?", "", text).strip()
    text = re.sub(r"```$", "", text).strip()
    data = json.loads(text)

    interpreted = data.get("interpreted_answer", "UNKNOWN")
    if interpreted not in ("YES", "NO", "UNKNOWN"):
        interpreted = "UNKNOWN"

    mentioned = data.get("mentioned_symptoms", [])
    if not isinstance(mentioned, list):
        mentioned = []

    return interpreted, [str(s) for s in mentioned]


# --- Conservative fallback used only when Gemini is not configured ---------

_YES_WORDS = {
    "yes", "y", "yeah", "yup", "aama", "amma", "aamaam", "irukku", "irukthu",
    "iruku", "unga", "ok", "iruntha",
}
_NO_WORDS = {
    "no", "n", "nope", "illa", "illai", "ille", "poidhu", "naan", "kidayathu",
}


def _fallback_interpret(question_text, patient_answer):
    normalized = (patient_answer or "").strip().lower()
    normalized = re.sub(r"[^a-z\s]", "", normalized)
    tokens = set(normalized.split())

    if tokens & _NO_WORDS:
        return "NO", []
    if tokens & _YES_WORDS:
        return "YES", []
    return "UNKNOWN", []


def interpret_answer(question, patient_answer, language="en"):
    """
    question: a question dict from questions.py (has 'text' and 'category')
    patient_answer: raw text of what the patient said (from Twilio speech-to-text,
                    or typed directly in the /analyze text-demo)
    language: hint only ("en" | "ta" | "tanglish") - Gemini is asked to understand
              meaning regardless, this is passed for context/logging.

    Returns: {
        "interpreted_answer": "YES" | "NO" | "UNKNOWN",
        "detected_symptoms": [category] if YES on this question else [],
        "mentioned_symptoms": [free-text symptom mentions from the model, may be empty],
        "engine": "gemini" | "fallback",
    }
    """
    question_text = question.get("text", {}).get(language) or question.get(
        "text", {}
    ).get("en", "")
    category = question.get("category")

    if not patient_answer or not patient_answer.strip():
        return {
            "interpreted_answer": "UNKNOWN",
            "detected_symptoms": [],
            "mentioned_symptoms": [],
            "engine": "none",
        }

    if _gemini_available:
        try:
            interpreted, mentioned = _call_gemini(question_text, patient_answer)
            engine = "gemini"
        except Exception:
            # Any failure (network, parsing, quota) -> fail safe to UNKNOWN,
            # never guess.
            interpreted, mentioned = "UNKNOWN", []
            engine = "gemini_error_fallback"
    else:
        interpreted, mentioned = _fallback_interpret(question_text, patient_answer)
        engine = "fallback"

    detected_symptoms = [category] if (interpreted == "YES" and category) else []

    return {
        "interpreted_answer": interpreted,
        "detected_symptoms": detected_symptoms,
        "mentioned_symptoms": mentioned,
        "engine": engine,
    }


def is_gemini_configured():
    return _gemini_available
