import streamlit as st
from app.utils.pdf_parser import extract_text_from_pdf
from app.utils.summarize import summarize_contract
from app.utils.risk_scorer import score_contract_risk
import tempfile
import time
import os

# Configure page
st.set_page_config(page_title="Legal Lens", layout="wide", page_icon="📄")
st.title("📄 Legal Lens: Contract Analyzer")
st.caption("AI-powered contract risk assessment using Gemini 2.0 Flash")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    st.markdown("""
    **Tip:** For best results:
    - Use digital PDFs (not scanned)
    - Focus on key contract sections
    """)
    st.divider()
    debug_mode = st.toggle("Show debug info")

# Main content area
uploaded_file = st.file_uploader("Upload a PDF contract", type=["pdf"])

if uploaded_file:
    # File processing
    with st.spinner("Extracting text..."):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name
            
            extracted_text = extract_text_from_pdf(tmp_path)
            
            # Clean up temp file
            try:
                os.unlink(tmp_path)
            except:
                pass
            
            if extracted_text.startswith("PDF extraction error"):
                st.error("Failed to extract text. Please upload a valid PDF.")
                st.stop()
                
        except Exception as e:
            st.error(f"File processing error: {str(e)}")
            st.stop()
    
    st.success("✅ Text extracted successfully")
    
    # Debug view
    if debug_mode:
        with st.expander("🔍 Raw Extracted Text"):
            st.text_area("Full Text", extracted_text, height=300)
    else:
        with st.expander("🔍 Text Preview"):
            st.text_area("First 500 characters", extracted_text[:500], height=150)

    # Analysis columns
    col1, col2 = st.columns(2)
    
    with col1:
        with st.spinner("Generating summary..."):
            time.sleep(1)  # Rate limiting
            summary = summarize_contract(extracted_text)
            
        if summary:
            st.markdown("### 🧠 Contract Summary")
            
            # Try to parse structured output
            if "### Key Risks" in summary:
                summary_part = summary.split("### Key Risks")[0]
                risks_part = summary.split("### Key Risks")[1].split("### Action Items")[0]
                actions_part = summary.split("### Action Items")[1] if "### Action Items" in summary else ""
                
                st.markdown(summary_part)
                
                with st.expander("⚠️ Key Risks"):
                    st.markdown(risks_part)
                
                if actions_part:
                    with st.expander("✅ Recommended Actions"):
                        st.markdown(actions_part)
            else:
                st.markdown(summary)
        else:
            st.warning("Summarization failed - the contract may be too short or complex.")

    with col2:
        with st.spinner("Calculating risk..."):
            time.sleep(1)  # Rate limiting
            risk = score_contract_risk(extracted_text)
            
        if risk != -1:
            st.markdown("### ⚠️ Risk Assessment")
            
            # Color-coded risk display
            if risk >= 7:
                risk_color = "red"
                risk_emoji = "🚨"
                risk_text = "High Risk"
            elif risk >= 4:
                risk_color = "orange"
                risk_emoji = "⚠️"
                risk_text = "Moderate Risk"
            else:
                risk_color = "green"
                risk_emoji = "✅"
                risk_text = "Low Risk"
                
            st.markdown(f"""
            <div style="text-align: center">
                <h1 style="color: {risk_color}">{risk_emoji} {risk}/10</h1>
                <h3 style="color: {risk_color}">{risk_text}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            st.progress(risk / 10)
            
            # Risk interpretation
            st.markdown("""
            **Risk Scale:**
            - 0-3: Standard/low-risk terms
            - 4-6: Some concerning clauses
            - 7-10: Significant risks present
            """)
        else:
            st.error("Risk scoring failed - please try again.")

# Add footer
st.divider()
st.caption("""
ℹ️ Note: This tool provides preliminary analysis only. 
Always consult a qualified attorney for legal advice.
""")