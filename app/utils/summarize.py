from dotenv import load_dotenv
import os
import google.generativeai as genai
from typing import Optional

# Configuration (runs once at startup)
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = genai.GenerativeModel("gemini-2.0-flash")

def summarize_contract(text: str, max_length: int = 1500) -> Optional[str]:
    """
    MVP contract summarizer with risk highlighting.
    Returns None if summarization fails.

    """

    prompt = f"""
    **Analyze this legal contract and provide structured output:**

    **Contract Excerpt:** {text[:15000]}

    **Required Output Format:**

    1. **Summary** (Plain English):
    - [3-5 sentence overview of key terms]

    2. **Key Risks** (Prioritized):
    - [Risk 1]: [Description] (Page [X] if detectable)
    - [Risk 2]: [Description] (Page [Y] if detectable)
    - [Risk 3]: [Description] (Page [Z] if detectable)

    3. **Action Items**:
     - [Recommended action 1]
     - [Recommended action 2]

    **Focus Areas:**
    - Automatic renewal clauses
    - Liability limitations
    - Termination penalties
    - Unilateral modification rights
    - Unusual payment terms
    - Jurisdiction/arbitration clauses

    **Rules:**
    - Use bullet points for clarity
    - Highlight exact clause wording when possible
    - If page numbers can't be determined, omit them
    - Never invent clauses not present in the text

    """

    try:
        response = MODEL.generate_content(
            prompt,
            generation_config={"max_output_tokens": max_length}
        )
        return response.text
    except Exception as e:
        print(f"Gemini error: {e}")
        return None