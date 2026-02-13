import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODELS = [
    "models/gemini-2.5-flash",
    "models/gemini-flash-latest"
]

def generate_enhanced_resume(resume, jd):
    prompt = f"""
You are an ATS resume expert.

JOB DESCRIPTION:
{jd}

RESUME:
{resume}

Rewrite resume with:
- Strong action verbs
- Spaces between each section
- Quantified impact
- ATS optimization
- Clean professional formatting
Use ONLY plain text.
NO markdown.
NO emojis.
Use bullet points starting with "-".

ONLY OUTPUT RESUME
"""

    for m in MODELS:
        try:
            model = genai.GenerativeModel(m)
            res = model.generate_content(prompt)
            if res.text and len(res.text) > 300:
                return res.text
        except:
            pass

    return resume
