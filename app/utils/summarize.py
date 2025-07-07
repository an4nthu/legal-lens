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

**Contract Excerpt:**
{text[:15000]}

**Required Output Format:**

1. **Summary** (Comprehensive yet clear):
   - Start with the contract type and primary purpose (1 sentence)
   - Describe key obligations of each party (2-3 sentences)
   - Highlight duration, renewal, and termination terms (2 sentences)
   - Note any unusual or noteworthy provisions (1-2 sentences)

2. **Key Risks** (Prioritized top 3):
   - [❗] [Brief risk title]: [2 to 3 sentence description] (Page [X] if found)

3. **Action Items** (Immediate next steps):
   - [🔍] [Specific clause to review]
   - [✍️] [Suggested negotiation point]
   - [⚠️] [Critical warning if applicable]

**Focus Areas:**
- Automatic renewals → Cancellation windows
- Liability caps → Reasonableness
- Termination → Penalties/notice periods
- Modifications → Unilateral changes
- Payments → Hidden fees/schedule
- Disputes → Governing law/arbitration

**Strict Rules:**
1. Summary must be 6-8 sentences total
2. Each risk limited to 1 line
3. Action items must begin with icon (🔍/✍️/⚠️)
4. Never infer clauses not explicitly stated
5. Use plain language (no legalese)
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