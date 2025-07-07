import fitz  # PyMuPDF

def extract_text_from_pdf(file_path: str) -> str:
    """MVP text extraction with minimal error handling."""
    try:
        text = []
        with fitz.open(file_path) as doc:
            for page in doc:
                if text_chunk := page.get_text():  # Walrus operator for conciseness
                    text.append(text_chunk)
        return "\n".join(text) if text else "No text found"
    
    except Exception as e:
        # Return error as string (simplest MVP approach)
        return f"PDF extraction error: {str(e)}"