"""
Q01-Q20 maternal health screening questions.

Each question has:
  id            - stable identifier, referenced everywhere else (answers, risk rules)
  category      - symptom category used by risk_rules.py
  text          - dict of {en, ta, tanglish} phrasing for Twilio TTS / frontend display
  emergency     - True if a YES answer here should be treated as a potential emergency signal
  follow_ups    - list of extra questions asked ONLY if the main question is answered YES.
                  Each follow-up has the same shape (id, category, text) but no nested follow_ups
                  to keep the engine simple for a 24h hackathon.

NOTE: This is a hackathon prototype question set for screening purposes only.
It is NOT a validated clinical instrument, does not diagnose any condition, and
must always be paired with guidance to contact a qualified healthcare professional.
"""

QUESTIONS = [
    {
        "id": "Q01",
        "category": "bleeding",
        "emergency": True,
        "text": {
            "en": "Have you had any vaginal bleeding recently?",
            "ta": "சமீபத்தில் யோனி வழியாக இரத்தப்போக்கு ஏற்பட்டதா?",
            "tanglish": "Recent-a bleeding edunda?",
        },
        "follow_ups": [
            {
                "id": "Q01F1",
                "category": "bleeding",
                "text": {
                    "en": "Is the bleeding heavy, like soaking through a pad quickly?",
                    "ta": "இரத்தப்போக்கு அதிகமாக, விரைவாக பேட் நனையும் அளவுக்கு இருக்கிறதா?",
                    "tanglish": "Bleeding heavy-a irukka, pad quick-a soak aaguma?",
                },
            }
        ],
    },
    {
        "id": "Q02",
        "category": "headache",
        "emergency": False,
        "text": {
            "en": "Have you had a severe headache in the last day?",
            "ta": "கடந்த ஒரு நாளில் கடுமையான தலைவலி இருந்ததா?",
            "tanglish": "Semma headache last one day-la irundhicha?",
        },
        "follow_ups": [
            {
                "id": "Q02F1",
                "category": "headache",
                "text": {
                    "en": "Does the headache come with blurred vision or seeing spots?",
                    "ta": "தலைவலியுடன் பார்வை மங்கல் அல்லது புள்ளிகள் தெரிவது இருக்கிறதா?",
                    "tanglish": "Headache kooda vision blur agitha or spots therikutha?",
                },
            }
        ],
    },
    {
        "id": "Q03",
        "category": "vision",
        "emergency": True,
        "text": {
            "en": "Have you noticed any blurred vision or other vision problems?",
            "ta": "பார்வை மங்கல் அல்லது வேறு பார்வைப் பிரச்சனைகள் ஏதேனும் இருக்கிறதா?",
            "tanglish": "Vision blur ah edhavadhu vision problem irukka?",
        },
        "follow_ups": [],
    },
    {
        "id": "Q04",
        "category": "abdominal_pain",
        "emergency": True,
        "text": {
            "en": "Do you have severe or constant abdominal pain?",
            "ta": "கடுமையான அல்லது தொடர்ச்சியான வயிற்று வலி இருக்கிறதா?",
            "tanglish": "Severe ah continuous ah stomach pain irukka?",
        },
        "follow_ups": [
            {
                "id": "Q04F1",
                "category": "abdominal_pain",
                "text": {
                    "en": "Is the pain constant, not coming and going like a contraction?",
                    "ta": "வலி தொடர்ச்சியாக இருக்கிறதா, சுருக்கம் போல வந்து போகிறதா இல்லையா?",
                    "tanglish": "Pain continuous-a irukka, contraction madhiri vandhu pogudha illaya?",
                },
            }
        ],
    },
    {
        "id": "Q05",
        "category": "fever",
        "emergency": False,
        "text": {
            "en": "Have you had a fever in the last two days?",
            "ta": "கடந்த இரண்டு நாட்களில் காய்ச்சல் இருந்ததா?",
            "tanglish": "Last 2 days-la fever irundhicha?",
        },
        "follow_ups": [],
    },
    {
        "id": "Q06",
        "category": "fetal_movement",
        "emergency": False,
        "text": {
            "en": "Have you noticed reduced or no baby movement compared to usual?",
            "ta": "வழக்கத்தை விட குழந்தையின் அசைவு குறைந்திருக்கிறதா அல்லது இல்லையா?",
            "tanglish": "Usual-a irundha vida baby movement kammiya irukka?",
        },
        "follow_ups": [],
    },
    {
        "id": "Q07",
        "category": "contractions",
        "emergency": False,
        "text": {
            "en": "Are you having regular contractions or tightening of the belly?",
            "ta": "வயிறு தொடர்ச்சியாக இறுக்கம் ஏற்படுகிறதா அல்லது சுருக்கங்கள் வருகிறதா?",
            "tanglish": "Regular ah contractions or stomach tightening irukka?",
        },
        "follow_ups": [
            {
                "id": "Q07F1",
                "category": "contractions",
                "text": {
                    "en": "Are these contractions less than 10 minutes apart?",
                    "ta": "இந்த சுருக்கங்கள் 10 நிமிடங்களுக்கும் குறைவான இடைவெளியில் வருகிறதா?",
                    "tanglish": "Contractions 10 minutes gap kammiya varudha?",
                },
            }
        ],
    },
    {
        "id": "Q08",
        "category": "breathlessness",
        "emergency": True,
        "text": {
            "en": "Do you feel severe breathlessness, even while resting?",
            "ta": "ஓய்வெடுக்கும்போது கூட கடுமையான மூச்சு விடும் சிரமம் இருக்கிறதா?",
            "tanglish": "Rest pannumbodhu kooda semma breathlessness irukka?",
        },
        "follow_ups": [],
    },
    {
        "id": "Q09",
        "category": "seizure",
        "emergency": True,
        "text": {
            "en": "Have you had any seizures, convulsions, or fainting?",
            "ta": "வலிப்பு, சிலிர்ப்பு அல்லது மயக்கம் ஏதேனும் ஏற்பட்டதா?",
            "tanglish": "Seizure, convulsion, ya fainting edhavadhu irundhicha?",
        },
        "follow_ups": [],
    },
    {
        "id": "Q10",
        "category": "vomiting",
        "emergency": False,
        "text": {
            "en": "Have you been vomiting persistently and unable to keep food or water down?",
            "ta": "தொடர்ந்து வாந்தி ஏற்பட்டு உணவு அல்லது தண்ணீர் நிற்காமல் இருக்கிறதா?",
            "tanglish": "Continuous ah vomiting, food water keep panna mudiyala-nu irukka?",
        },
        "follow_ups": [],
    },
    {
        "id": "Q11",
        "category": "urinary",
        "emergency": False,
        "text": {
            "en": "Do you feel burning or pain while urinating?",
            "ta": "சிறுநீர் கழிக்கும்போது எரிச்சல் அல்லது வலி இருக்கிறதா?",
            "tanglish": "Urine pannumbodhu burning or pain irukka?",
        },
        "follow_ups": [],
    },
    {
        "id": "Q12",
        "category": "fluid_leak",
        "emergency": False,
        "text": {
            "en": "Have you noticed any fluid leaking from below, other than urine?",
            "ta": "சிறுநீர் அல்லாமல் வேறு ஏதேனும் திரவம் கசிவது இருக்கிறதா?",
            "tanglish": "Urine illama vera edhavadhu fluid leak agudha?",
        },
        "follow_ups": [],
    },
    {
        "id": "Q13",
        "category": "back_pain",
        "emergency": False,
        "text": {
            "en": "Are you having severe lower back pain?",
            "ta": "கடுமையான இடுப்பு வலி இருக்கிறதா?",
            "tanglish": "Semma lower back pain irukka?",
        },
        "follow_ups": [],
    },
    {
        "id": "Q14",
        "category": "dizziness",
        "emergency": False,
        "text": {
            "en": "Do you feel dizzy or like you might faint?",
            "ta": "தலைச்சுற்றல் அல்லது மயங்கிவிடுவது போல் உணர்கிறீர்களா?",
            "tanglish": "Dizzy ah illa fainting madhiri feel aaguma?",
        },
        "follow_ups": [],
    },
    {
        "id": "Q15",
        "category": "swelling",
        "emergency": False,
        "text": {
            "en": "Have you noticed sudden swelling in your face, hands, or feet?",
            "ta": "முகம், கைகள் அல்லது கால்களில் திடீர் வீக்கம் இருக்கிறதா?",
            "tanglish": "Face, hands, ya feet-la sudden swelling irukka?",
        },
        "follow_ups": [],
    },
    {
        "id": "Q16",
        "category": "appetite",
        "emergency": False,
        "text": {
            "en": "Have you had trouble eating well or noticed a big change in appetite?",
            "ta": "சாப்பிடுவதில் சிரமம் அல்லது பசியில் பெரிய மாற்றம் இருக்கிறதா?",
            "tanglish": "Sapada trouble irukka illa appetite-la periya maatram irukka?",
        },
        "follow_ups": [],
    },
    {
        "id": "Q17",
        "category": "sleep",
        "emergency": False,
        "text": {
            "en": "Are you having serious trouble sleeping?",
            "ta": "தூக்கத்தில் கடுமையான சிரமம் இருக்கிறதா?",
            "tanglish": "Sleep panna semma trouble irukka?",
        },
        "follow_ups": [],
    },
    {
        "id": "Q18",
        "category": "mental_health",
        "emergency": False,
        "text": {
            "en": "Have you been feeling very low, anxious, or overwhelmed lately?",
            "ta": "சமீபத்தில் மிகவும் மனச்சோர்வு, பதற்றம் அல்லது சோர்வாக உணர்கிறீர்களா?",
            "tanglish": "Recent-a semma low ah, anxious ah, illa overwhelmed ah feel aaguma?",
        },
        "follow_ups": [],
    },
    {
        "id": "Q19",
        "category": "history",
        "emergency": False,
        "text": {
            "en": "Have you had any complications in a previous pregnancy?",
            "ta": "முந்தைய கர்ப்ப காலத்தில் ஏதேனும் சிக்கல்கள் இருந்ததா?",
            "tanglish": "Previous pregnancy-la edhavadhu complication irundhicha?",
        },
        "follow_ups": [],
    },
    {
        "id": "Q20",
        "category": "general_wellbeing",
        "emergency": False,
        "text": {
            "en": "Overall, is there anything else about your health today that is worrying you?",
            "ta": "மொத்தத்தில், இன்று உங்கள் ஆரோக்கியத்தில் வேறு ஏதேனும் கவலை இருக்கிறதா?",
            "tanglish": "Overall, indha health-la vera edhavadhu worry irukka?",
        },
        "follow_ups": [],
    },
]

QUESTIONS_BY_ID = {}
for _q in QUESTIONS:
    QUESTIONS_BY_ID[_q["id"]] = _q
    for _fu in _q.get("follow_ups", []):
        QUESTIONS_BY_ID[_fu["id"]] = _fu


def get_question_text(question, lang="en"):
    """Return the question's text in the requested language, falling back to English."""
    texts = question.get("text", {})
    return texts.get(lang) or texts.get("en") or ""
