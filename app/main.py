from fastapi import FastAPI, UploadFile, File

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
    return {"filename": file.filename}
