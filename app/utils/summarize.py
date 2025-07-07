from dotenv import load_dotenv
import os
import google.generativeai as genai
from typing import Optional

# Configuration (runs once at startup)
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = genai.GenerativeModel("gemini-1.5-flash")

def summarize_contract(text: str, max_length: int = 1500) -> Optional[str]:
    """
    MVP contract summarizer with risk highlighting.
    Returns None if summarization fails.
    """
    prompt = f"""Analyze this legal contract and provide:
    1. A 3-5 sentence plain English summary
    2. List of 3-5 most risky/unfair clauses 
    3. Page numbers where risks occur (if detectable)
    
    Focus on:
    - Automatic renewals
    - Liability limitations
    - Termination penalties
    - Unilateral modification clauses
    
    Contract Text:\n{text[:15000]}"""  # Truncate to avoid token limits

    try:
        response = MODEL.generate_content(
            prompt,
            generation_config={"max_output_tokens": max_length}
        )
        return response.text
    except Exception as e:
        print(f"Gemini error: {e}")
        return None