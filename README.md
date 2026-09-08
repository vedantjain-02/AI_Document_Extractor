# 🤖 AI Document Extractor

An AI-powered document processing system that extracts structured information from documents using **PaddleOCR**, **document-type detection**, and **Groq AI**.

The project is designed to process different types of documents such as **PAN Card, Aadhaar Card, Passport**, and unknown documents like driving licences.

---

## 🚀 Features

- 📄 Upload documents through a simple Streamlit interface
- 🔍 OCR using PaddleOCR
- 🧠 Automatic document type detection
- 🤖 AI-powered information extraction using Groq
- 🪪 PAN Card data extraction
- 🆔 Aadhaar Card data extraction
- 🌍 Passport data extraction
- 📋 Generic extraction for unknown documents
- 📦 Structured JSON output
- 👀 Document preview
- 📝 OCR text display
- ⚡ FastAPI backend
- 🎨 Professional Streamlit frontend

---

## 🏗️ System Architecture

```text
                 ┌─────────────────┐
                 │   User Upload   │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │   Streamlit UI  │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │   FastAPI API   │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │    PaddleOCR    │
                 │ Text Extraction │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │ Document Type   │
                 │    Detection    │
                 └────────┬────────┘
                          │
             ┌────────────┴────────────┐
             │                         │
             ▼                         ▼
      Known Documents            Unknown Document
      PAN/Aadhaar/Passport       Groq AI Extraction
             │                         │
             └────────────┬────────────┘
                          ▼
                 ┌─────────────────┐
                 │ Structured JSON │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │   Frontend UI   │
                 └─────────────────┘
```

---

## 📁 Project Structure

```text
AI_Document_Extractor/
│
├── backend/
│   ├── .venv/
│   ├── uploads/
│   │
│   ├── main.py
│   ├── ocr_service.py
│   ├── document_detector.py
│   ├── extractor_router.py
│   │
│   ├── pan_extractor.py
│   ├── aadhaar_extractor.py
│   ├── passport_extractor.py
|   ├── generic_extractor.py
│   ├── grok_service.py
│   │
│   └── requirements.txt
│
├── frontend/
│   └── app.py
│
├── README.md
└── .gitignore
```

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend development |
| FastAPI | REST API |
| PaddleOCR | Optical Character Recognition |
| PaddlePaddle | OCR framework |
| Groq API | AI-based document extraction |
| Streamlit | Frontend |
| Regular Expressions | Pattern-based extraction |
| JSON | Structured output |

---

## 📄 Supported Documents

### PAN Card

Extracts:

- PAN Number
- Name
- Father's Name
- Date of Birth

### Aadhaar Card

Extracts:

- Aadhaar Number
- Name
- Date of Birth
- Year of Birth
- Gender

### Passport

Extracts:

- Passport Number
- Name
- Date of Birth
- Nationality
- Sex

### Unknown Documents

For documents that are not explicitly supported, the system can use AI to identify the document and extract relevant fields.

Example:

```json
{
  "document_type": "Driver's License",
  "data": {
    "license_number": "...",
    "name": "...",
    "date_of_birth": "...",
    "expiration_date": "..."
  }
}
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd AI_Document_Extractor
```

### 2. Create a virtual environment

```bash
cd backend
python -m venv .venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```bash
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file inside the `backend` folder:

```env
GROQ_API_KEY=your_groq_api_key_here
```

**Important:** Never upload your real API key to GitHub.

Add `.env` to `.gitignore`:

```text
.env
.venv/
__pycache__/
uploads/
```

---

## ▶️ Run the Backend

From the `backend` folder:

```bash
uvicorn main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

### Swagger API Documentation

Open:

```text
http://127.0.0.1:8000/docs
```

The `/upload` endpoint can be used to upload and process a document.

---

## 🎨 Run the Frontend

Open another terminal and go to the frontend directory:

```bash
cd frontend
```

Run Streamlit:

```bash
streamlit run app.py
```

The frontend will normally open at:

```text
http://localhost:8501
```

---

## 🔄 Processing Pipeline

The application follows this pipeline:

```text
Upload Document
       ↓
PaddleOCR
       ↓
Extract Text
       ↓
Document Type Detection
       ↓
Document-Specific Extraction
       ↓
Groq AI for Generic Documents
       ↓
Structured JSON
       ↓
Display Result
```

---

## 📡 API Example

### Upload Document

**Endpoint:**

```text
POST /upload
```

The API accepts a document file and returns structured information.

Example response:

```json
{
  "filename": "document.jpg",
  "document_type": "PAN Card",
  "data": {
    "pan_number": "XXXXXXXXXX",
    "name": "Example Name",
    "father_name": "Example Father",
    "date_of_birth": "DD/MM/YYYY"
  },
  "extracted_text": []
}
```

Sensitive document values should be kept private and should not be committed to source control.

---

## 🧠 How It Works

### 1. OCR

PaddleOCR reads text from the uploaded document.

### 2. Document Detection

The extracted text is analyzed to determine whether the document is:

- PAN Card
- Aadhaar Card
- Passport
- Unknown

### 3. Structured Extraction

Known document types use dedicated Python extractors.

For example:

```text
PAN → pan_extractor.py
Aadhaar → aadhaar_extractor.py
Passport → passport_extractor.py
```

### 4. AI Extraction

Unknown documents are processed using the Groq API to identify the document and extract relevant information dynamically.

---

## 🧪 Testing

Backend health check:

```text
GET /
```

Expected response:

```json
{
  "message": "AI Document Extractor API is running 🚀"
}
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

Frontend:

```text
http://localhost:8501
```

---

## 🔒 Security Notes

This project can process sensitive identity documents. For real-world deployment:

- Never expose API keys in source code.
- Never commit `.env` files.
- Avoid storing uploaded identity documents permanently.
- Use HTTPS in production.
- Restrict access to uploaded files.
- Delete temporary files after processing.
- Do not log sensitive document numbers.
- Use redacted/dummy documents for public demonstrations.

---

## 🚧 Future Improvements

Planned improvements include:

- ✨ AI-powered OCR cleanup
- 📑 Support for more document types
- 🌐 Better multilingual OCR
- 🎯 Confidence scores
- 🔎 Improved document detection
- 🧩 More robust field extraction
- 📊 Extraction history
- 👤 User authentication
- ☁️ Cloud deployment
- 🗃️ Database integration
- 📱 Responsive frontend
- 🔐 Production-grade security

---

## 👨‍💻 Author

**Vedant Jain**

AI / Python Developer

---

## ⭐ Project Goal

The goal of this project is to build a **general-purpose AI Document Extraction system** capable of converting unstructured document images into clean, structured and machine-readable information.

```text
Document Image
      ↓
      OCR
      ↓
   AI Analysis
      ↓
Structured Data
```

---

## 📜 License

This project is intended for educational and development purposes.
