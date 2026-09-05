QUESTIONS = {

    "Q01": {
        "name": "Vaginal bleeding/spotting",
        "keywords": [
            "bleeding",
            "spotting",
            "blood"
        ],
        "action": "Escalation"
    },

    "Q02": {
        "name": "Severe/persistent headache",
        "keywords": [
            "headache",
            "head pain",
            "bad headache",
            "severe headache",
            "head is hurting"
        ],
        "action": "Urgent review"
    },

    "Q03": {
        "name": "Blurred vision/flashes/vision loss",
        "keywords": [
            "blurred vision",
            "blurry vision",
            "vision is blurry",
            "flashes",
            "vision loss",
            "cannot see"
        ],
        "action": "Immediate clinical escalation"
    },

    "Q04": {
        "name": "Severe/constant abdominal pain",
        "keywords": [
            "abdominal pain",
            "stomach pain",
            "belly pain",
            "severe stomach pain",
            "constant stomach pain"
        ],
        "action": "Immediate clinical escalation"
    },

    "Q05": {
        "name": "Fluid leakage/gushing",
        "keywords": [
            "fluid leakage",
            "fluid leaking",
            "water leaking",
            "water is leaking",
            "gushing"
        ],
        "action": "Urgent escalation"
    },

    "Q06": {
        "name": "Breathlessness at rest",
        "keywords": [
            "breathless",
            "breathlessness",
            "difficulty breathing",
            "hard to breathe",
            "shortness of breath"
        ],
        "action": "Immediate clinical review"
    },

    "Q07": {
        "name": "Fever/chills",
        "keywords": [
            "fever",
            "high temperature",
            "temperature",
            "chills",
            "feeling cold and shivering"
        ],
        "action": "Clinical review"
    },

    "Q08": {
        "name": "Convulsions/fainting",
        "keywords": [
            "convulsion",
            "seizure",
            "fainting",
            "fainted",
            "passed out"
        ],
        "action": "Immediate escalation"
    },

    "Q09": {
        "name": "Reduced fetal movement",
        "keywords": [
            "baby not moving",
            "baby is not moving",
            "less baby movement",
            "reduced fetal movement",
            "reduced movement",
            "baby movement decreased"
        ],
        "action": "Same-day assessment"
    },

    "Q10": {
        "name": "Face/hand swelling",
        "keywords": [
            "face swelling",
            "swollen face",
            "hand swelling",
            "swollen hands",
            "hands are swollen"
        ],
        "action": "Clinical review"
    },

    "Q11": {
        "name": "Pain/burning while urinating",
        "keywords": [
            "burning urination",
            "burning while urinating",
            "pain urinating",
            "pain while urinating",
            "burning urine"
        ],
        "action": "Follow-up"
    },

    "Q12": {
        "name": "Unable to keep food/water down",
        "keywords": [
            "cannot keep food down",
            "can't keep food down",
            "cannot keep water down",
            "can't keep water down",
            "vomiting continuously",
            "throwing up"
        ],
        "action": "Prompt review"
    },

    "Q13": {
        "name": "Regular painful contractions",
        "keywords": [
            "contractions",
            "painful contractions",
            "regular contractions",
            "contraction pain"
        ],
        "action": "Escalation according to protocol"
    },

    "Q14": {
        "name": "Weakness/dizziness/palpitations",
        "keywords": [
            "weakness",
            "feeling weak",
            "dizziness",
            "dizzy",
            "palpitations",
            "heart racing"
        ],
        "action": "Clinical review"
    },

    "Q15": {
        "name": "Iron/calcium adherence",
        "keywords": [
            "iron tablets",
            "iron medicine",
            "calcium tablets",
            "calcium medicine",
            "taking iron",
            "taking calcium"
        ],
        "action": "Reminder/follow-up"
    },

    "Q16": {
        "name": "Back/hip pain",
        "keywords": [
            "back pain",
            "lower back pain",
            "hip pain",
            "pain in my back"
        ],
        "action": "Routine/clinical review"
    },

    "Q17": {
        "name": "Sadness/hopelessness/anxiety",
        "keywords": [
            "sad",
            "feeling sad",
            "hopeless",
            "hopelessness",
            "anxiety",
            "anxious",
            "worried all the time"
        ],
        "action": "Human follow-up"
    },

    "Q18": {
        "name": "Sleep problems",
        "keywords": [
            "can't sleep",
            "cannot sleep",
            "sleep problems",
            "trouble sleeping",
            "not sleeping",
            "insomnia"
        ],
        "action": "Routine"
    },

    "Q19": {
        "name": "One-sided calf swelling/pain",
        "keywords": [
            "calf swelling",
            "calf pain",
            "leg swelling",
            "one leg swollen",
            "one sided leg swelling",
            "one leg pain"
        ],
        "action": "Prompt review"
    },

    "Q20": {
        "name": "Nutrition",
        "keywords": [
            "nutrition",
            "diet",
            "healthy food",
            "eating",
            "food"
        ],
        "action": "Education/follow-up"
    }
}
QUESTIONS = {

    "Q01": {
        "name": "Vaginal bleeding/spotting",
        "keywords": [
            "bleeding",
            "spotting",
            "blood",
            "vaginal bleeding",
            "vaginal spotting"
        ],
        "context": (
            "Requires clinical assessment. "
            "Severity and context determine urgency."
        ),
        "action": "Escalation"
    },

    "Q02": {
        "name": "Severe/persistent headache",
        "keywords": [
            "headache",
            "head pain",
            "bad headache",
            "severe headache",
            "persistent headache",
            "head is hurting",
            "head hurts"
        ],
        "context": (
            "Higher urgency when associated with visual symptoms "
            "or other concerning findings."
        ),
        "action": "Urgent review"
    },

    "Q03": {
        "name": "Blurred vision/flashes/vision loss",
        "keywords": [
            "blurred vision",
            "blurry vision",
            "vision is blurry",
            "vision blurry",
            "flashes",
            "flashing lights",
            "vision loss",
            "lost vision",
            "cannot see",
            "can't see"
        ],
        "context": (
            "Red flag symptom."
        ),
        "action": "Immediate clinical escalation"
    },

    "Q04": {
        "name": "Severe/constant abdominal pain",
        "keywords": [
            "abdominal pain",
            "stomach pain",
            "belly pain",
            "severe stomach pain",
            "constant stomach pain",
            "severe abdominal pain",
            "constant abdominal pain"
        ],
        "context": (
            "Red flag symptom."
        ),
        "action": "Immediate clinical escalation"
    },

    "Q05": {
        "name": "Fluid leakage/gushing",
        "keywords": [
            "fluid leakage",
            "fluid leaking",
            "water leaking",
            "water is leaking",
            "water leakage",
            "gushing",
            "fluid gushing"
        ],
        "context": (
            "Requires prompt assessment. "
            "Gestational age matters."
        ),
        "action": "Urgent escalation"
    },

    "Q06": {
        "name": "Breathlessness at rest",
        "keywords": [
            "breathless",
            "breathlessness",
            "difficulty breathing",
            "hard to breathe",
            "shortness of breath",
            "cannot breathe",
            "can't breathe",
            "breathing difficulty"
        ],
        "context": (
            "Red flag/high-priority symptom."
        ),
        "action": "Immediate clinical review"
    },

    "Q07": {
        "name": "Fever/chills",
        "keywords": [
            "fever",
            "high temperature",
            "temperature",
            "chills",
            "shivering",
            "feeling feverish"
        ],
        "context": (
            "Severity, temperature and associated symptoms matter."
        ),
        "action": "Clinical review"
    },

    "Q08": {
        "name": "Convulsions/fainting",
        "keywords": [
            "convulsion",
            "convulsions",
            "seizure",
            "seizures",
            "fainting",
            "fainted",
            "passed out",
            "lost consciousness"
        ],
        "context": (
            "Convulsions require an emergency pathway."
        ),
        "action": "Immediate escalation"
    },

    "Q09": {
        "name": "Reduced fetal movement",
        "keywords": [
            "baby not moving",
            "baby is not moving",
            "less baby movement",
            "reduced fetal movement",
            "reduced movement",
            "baby movement decreased",
            "baby moving less",
            "baby moves less",
            "less movement of baby"
        ],
        "context": (
            "Compare with the mother's usual pattern."
        ),
        "action": "Same-day assessment"
    },

    "Q10": {
        "name": "Face/hand swelling",
        "keywords": [
            "face swelling",
            "swollen face",
            "facial swelling",
            "hand swelling",
            "swollen hands",
            "hands are swollen",
            "swelling in hands",
            "swelling in face"
        ],
        "context": (
            "Combine with headache, vision and "
            "blood-pressure information."
        ),
        "action": "Clinical review"
    },

    "Q11": {
        "name": "Pain/burning while urinating",
        "keywords": [
            "burning urination",
            "burning while urinating",
            "pain urinating",
            "pain while urinating",
            "burning urine",
            "pain when urinating",
            "pain during urination",
            "burning when i pee",
            "burning when peeing"
        ],
        "context": (
            "Assess severity and associated fever/back pain."
        ),
        "action": "Follow-up"
    },

    "Q12": {
        "name": "Unable to keep food/water down",
        "keywords": [
            "cannot keep food down",
            "can't keep food down",
            "cannot keep water down",
            "can't keep water down",
            "vomiting continuously",
            "throwing up",
            "constant vomiting",
            "keep vomiting",
            "unable to eat",
            "unable to drink"
        ],
        "context": (
            "Assess dehydration and severity."
        ),
        "action": "Prompt review"
    },

    "Q13": {
        "name": "Regular painful contractions",
        "keywords": [
            "contractions",
            "painful contractions",
            "regular contractions",
            "contraction pain",
            "regular painful contractions",
            "labor contractions",
            "labour contractions"
        ],
        "context": (
            "Gestational age, frequency and duration are required."
        ),
        "action": "Escalation according to protocol"
    },

    "Q14": {
        "name": "Weakness/dizziness/palpitations",
        "keywords": [
            "weakness",
            "feeling weak",
            "dizziness",
            "dizzy",
            "lightheaded",
            "light headed",
            "palpitations",
            "heart racing",
            "heart beating fast"
        ],
        "context": (
            "Assess severity and associated symptoms."
        ),
        "action": "Clinical review"
    },

    "Q15": {
        "name": "Iron/calcium adherence",
        "keywords": [
            "iron tablets",
            "iron medicine",
            "iron supplement",
            "calcium tablets",
            "calcium medicine",
            "calcium supplement",
            "taking iron",
            "taking calcium",
            "iron tablet",
            "calcium tablet"
        ],
        "context": (
            "Preventive tracking, not emergency scoring."
        ),
        "action": "Reminder/follow-up"
    },

    "Q16": {
        "name": "Back/hip pain",
        "keywords": [
            "back pain",
            "lower back pain",
            "hip pain",
            "pain in my back",
            "pain in my lower back",
            "back ache",
            "backache"
        ],
        "context": (
            "Assess severity and associated symptoms."
        ),
        "action": "Routine/clinical review"
    },

    "Q17": {
        "name": "Sadness/hopelessness/anxiety",
        "keywords": [
            "sad",
            "feeling sad",
            "very sad",
            "hopeless",
            "hopelessness",
            "anxiety",
            "anxious",
            "feeling anxious",
            "worried all the time",
            "constant worry",
            "depressed"
        ],
        "context": (
            "Mental-health screening pathway."
        ),
        "action": "Human follow-up"
    },

    "Q18": {
        "name": "Sleep problems",
        "keywords": [
            "can't sleep",
            "cannot sleep",
            "sleep problems",
            "trouble sleeping",
            "not sleeping",
            "insomnia",
            "difficulty sleeping",
            "sleep difficulty"
        ],
        "context": (
            "Baseline monitoring."
        ),
        "action": "Routine"
    },

    "Q19": {
        "name": "One-sided calf swelling/pain",
        "keywords": [
            "calf swelling",
            "calf pain",
            "leg swelling",
            "one leg swollen",
            "one sided leg swelling",
            "one-sided leg swelling",
            "one leg pain",
            "swollen calf",
            "painful calf",
            "swelling in one leg"
        ],
        "context": (
            "Concerning clot symptom requiring clinical assessment."
        ),
        "action": "Prompt review"
    },

    "Q20": {
        "name": "Nutrition",
        "keywords": [
            "nutrition",
            "diet",
            "healthy food",
            "healthy eating",
            "eating",
            "food",
            "what should i eat",
            "what to eat",
            "pregnancy diet"
        ],
        "context": (
            "Preventive monitoring."
        ),
        "action": "Education/follow-up"
    }
}
