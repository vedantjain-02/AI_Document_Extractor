from fastapi import FastAPI,  UploadFile, File
from ocr_service import extract_text
import os
from extractor_router import extract_document_data
from document_detector import detect_document_type
from grok_service import test_grok, list_models

app = FastAPI(
    title="AI Document Extractor",
    description="Document Information Extraction API",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "AI Document Extractor API is running 🚀"
    }

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)

    file_path = os.path.join("uploads", file.filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    extracted_text = extract_text(file_path)

    document_type = detect_document_type(extracted_text)

    document_data = extract_document_data(
        document_type,
        extracted_text
    )

    if document_type == "Unknown" and isinstance(document_data, dict):
        document_type = document_data.get("document_type", "Unknown")

    return {
        "filename": file.filename,
        "document_type": document_type,
        "data": document_data.get("data", document_data),
        "extracted_text": extracted_text
    }