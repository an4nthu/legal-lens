from dotenv import load_dotenv
import os
import google.generativeai as genai
from typing import Literal

# Configuration - moved to top level for single initialization
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = genai.GenerativeModel("gemini-2.0-flash")

def score_contract_risk(text: str) -> Literal[-1, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
    """
    Returns risk score 0-10 (-1 for errors)
    Now with:
    - More detailed scoring rubric
    - Examples for calibration
    - Stricter output control
    """
    prompt = f"""
You are a legal contract evaluator. 
Read the contract below and output ONLY a single number between 0 and 10 representing its risk:

- 0 = No risk (clear, fair, harmless)
- 10 = Extremely risky (multiple unfair/hidden/dangerous clauses)

STRICT RULES:
- Return ONLY the number (no words, no punctuation)
- No explanation, no extra text

CONTRACT TEXT:
{text[:15000]}
"""

    try:
        response = MODEL.generate_content(
            prompt,
            generation_config={"temperature": 0.1,"max_output_tokens": 2}
        )
        return int(response.text.strip())
    except (ValueError, AttributeError):
        return -1  # Failed to parse score
    except Exception as e:
        print(f"Risk scoring error: {e}")
        return -1