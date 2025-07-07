from fastapi import FastAPI, UploadFile, HTTPException, File
import shutil
import os
from utils.pdf_parser import extract_text_from_pdf # Import the PDF text extraction function
from utils.summarize import summarize_contract


# This block allows running the FastAPI app directly with 'python main.py'
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True) # Run the FastAPI app named 'app' from 'main.py', with auto-reload

app = FastAPI() # Initialize the FastAPI application

@app.get("/") # Define a GET endpoint for the root URL "/"
async def root():
    return {"message": "Legal Lens API running"} # Return a simple JSON message

@app.post("/upload/") # Define a POST endpoint for file uploads at "/upload/"
async def upload_file(file: UploadFile = File(...)): # Expect an uploaded file named 'file'
    # Check if the uploaded file is a PDF; raise an error if not
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")
    
    file_location = f"temp_{file.filename}" # Create a temporary path to save the uploaded file
    # Save the uploaded file content to the temporary path
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    extracted_text = extract_text_from_pdf(file_location) # Extract text from the saved PDF using the utility function
    summary = summarize_contract(extracted_text) #summarize the extracted test using utility function


    os.unlink(file_location) # Delete the temporary PDF file after extraction

    # Return the filename, a 500-character preview of the extracted text, and its total length
    return {
        "filename": file.filename,
        "extracted_text": extracted_text[:500], # Slice to get only the first 500 characters
        "text_length": len(extracted_text),
        "summary": summary
    }