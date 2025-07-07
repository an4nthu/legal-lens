from fastapi import FastAPI, UploadFile, HTTPException, File
import shutil
import os
from utils.pdf_parser import extract_text_from_pdf

# Add this at the top of main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Legal Lens API running"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    
    file_location = f"temp_{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # extract text
    extracted_text = extract_text_from_pdf(file_location)

    os.unlink(file_location)

    # preview only first 500 chars to avoid flooding the response
    return {
        "filename": file.filename,
        "extracted_text": extracted_text[:500],
        "text_length": len(extracted_text)
    }

