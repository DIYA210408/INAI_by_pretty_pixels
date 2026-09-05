import os
from dotenv import load_dotenv
from google import genai

# Load the .env file
load_dotenv()

# Get the Gemini API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found. "
        "Please check your .env file."
    )

# Create Gemini client
client = genai.Client(api_key=api_key)


def ask_gemini(user_text: str):
    """
    Send the user's message to Gemini and identify
    which pregnancy symptom categories are relevant.
    """

    prompt = f"""
You are an assistant for a pregnancy symptom screening application.

The user's message is:

"{user_text}"

Identify which of these symptom categories are mentioned:

Q01 - Vaginal bleeding/spotting
Q02 - Severe/persistent headache
Q03 - Blurred vision/flashes/vision loss
Q04 - Severe/constant abdominal pain
Q05 - Fluid leakage/gushing
Q06 - Breathlessness at rest
Q07 - Fever/chills
Q08 - Convulsions/fainting
Q09 - Reduced fetal movement
Q10 - Face/hand swelling
Q11 - Pain/burning while urinating
Q12 - Unable to keep food/water down
Q13 - Regular painful contractions
Q14 - Weakness/dizziness/palpitations
Q15 - Iron/calcium adherence
Q16 - Back/hip pain
Q17 - Sadness/hopelessness/anxiety
Q18 - Sleep problems
Q19 - One-sided calf swelling/pain
Q20 - Nutrition

The user may communicate in English, Tamil, or Tanglish.

Understand the meaning of the user's message rather than
looking only for exact English keywords.

Return ONLY the relevant question IDs.

For example:
Q02, Q03

If none of the categories apply, return:
NONE
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text.strip()
