# 🤖 AI Document Extractor

An AI-powered document processing system that converts document images into structured, machine-readable information using **PaddleOCR, document-type detection, rule-based extraction, and Groq AI**.

The system can process documents such as **PAN Cards, Aadhaar Cards, and Passports**, extract important information, and allow users to interact with the uploaded document through an AI-powered **Document Q&A** interface.

---

## 🚀 Features

- 📄 Upload documents through a Streamlit interface
- 🔍 OCR using PaddleOCR
- 🧠 Automatic document-type detection
- 📦 Structured information extraction
- 🪪 PAN Card extraction
- 🆔 Aadhaar Card extraction
- 🌍 Passport extraction
- 🤖 Groq-powered Document Q&A
- 💬 Floating AI chat interface
- 🔎 OCR bounding-box detection
- 🔴 Highlight matching information directly on the document
- 📝 OCR text display
- 📋 Structured JSON output
- ⬇️ Download extracted JSON
- 👀 Document preview
- ⚡ FastAPI backend
- 🎨 Dark-themed Streamlit frontend
- 🔐 Environment-based API key management

---

# 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │      User Upload    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Streamlit UI      │
                    │    Frontend         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    FastAPI API      │
                    │      Backend        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     PaddleOCR       │
                    │  Text + Bounding    │
                    │      Boxes          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Document Type       │
                    │ Detection            │
                    └──────────┬──────────┘
                               │
              ┌────────────────┴────────────────┐
              │                                 │
              ▼                                 ▼
      Known Documents                    Unknown Documents
      PAN/Aadhaar/Passport                  Groq AI
              │                                 │
              ▼                                 ▼
      Dedicated Extractors              AI Extraction
              │                                 │
              └────────────────┬────────────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Structured JSON   │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 │                           │
                 ▼                           ▼
          Display Results              Document Q&A
                                             │
                                             ▼
                                        Groq AI
                                             │
                                             ▼
                                     Answer + Matching
                                      Bounding Boxes
                                             │
                                             ▼
                                    Highlighted Document
🔄 Processing Pipeline

The application follows an end-to-end AI document processing pipeline:

Document Upload
       ↓
     OCR
       ↓
Text + Bounding Boxes
       ↓
Document Type Detection
       ↓
Document-Specific Extraction
       ↓
Structured JSON
       ↓
Document Context
       ↓
AI Document Q&A
       ↓
Answer + Field Matching
       ↓
Bounding Box Highlighting
📁 Project Structure
AI_Document_Extractor/
│
├── backend/
│   │
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
│   ├── generic_extractor.py
│   │
│   ├── grok_service.py
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   └── app.py
│
├── README.md
├── LICENSE
└── .gitignore
🛠️ Technologies Used
Technology	Purpose
Python	Core development
FastAPI	Backend REST API
Uvicorn	ASGI server
PaddleOCR	Optical Character Recognition
PaddlePaddle	OCR framework
Groq API	AI-powered document Q&A
OpenAI Python SDK	Groq API integration
Streamlit	Frontend interface
Pillow	Image processing and bounding boxes
Requests	Frontend-backend communication
Regular Expressions	Pattern-based extraction
JSON	Structured data representation
📄 Supported Documents
🪪 PAN Card

The PAN extractor identifies and extracts:

PAN Number
Name
Father's Name
Date of Birth

Example:

{
    "pan_number": "XXXXXXXXXX",
    "name": "Example Name",
    "father_name": "Example Father",
    "date_of_birth": "DD/MM/YYYY"
}
🆔 Aadhaar Card

The Aadhaar extractor identifies:

Aadhaar Number
Name
Date of Birth
Year of Birth
Gender

Example:

{
    "aadhaar_number": "XXXX XXXX XXXX",
    "name": "Example Name",
    "date_of_birth": "DD/MM/YYYY",
    "year_of_birth": "YYYY",
    "gender": "Male"
}
🌍 Passport

The Passport extractor identifies:

Passport Number
Name
Date of Birth
Nationality
Sex

Example:

{
    "passport_number": "XXXXXXX",
    "name": "Example Name",
    "date_of_birth": "DD/MM/YYYY",
    "nationality": "IND",
    "sex": "M"
}
🤖 AI Document Q&A

The project includes an AI-powered Document Q&A system.

After uploading a document, users can open the floating chat button and ask questions about the uploaded document.

Example questions:

What is the date of birth?
What is the nationality?
What is the document number?

The AI uses the uploaded document's:

Document type
Structured extracted data
OCR text

to answer the question.

The AI is instructed to only use information available in the document and avoid generating unsupported information.

If the information cannot be found, the system responds:

I couldn't find that information in the document.
🔎 OCR Bounding Boxes

The OCR system does not only extract text.

It also stores the location of detected text using bounding-box coordinates.

Example:

{
    "text": "Example",
    "box": [290, 37, 368, 50]
}

These coordinates allow the application to connect an AI answer back to the original document.

🔴 Visual Field Highlighting

When a user asks a question through Document Q&A, the backend attempts to find the corresponding OCR text.

For example:

User:
What is the date of birth?

        ↓

Groq AI:
The date of birth is DD/MM/YYYY.

        ↓

OCR Matching

        ↓

Bounding Box

        ↓

Document Preview

        ↓

🔴 Matching field highlighted

This makes the system more transparent because the user can visually verify where the information came from.

🧠 How It Works
1. Document Upload

The user uploads a document from the Streamlit frontend.

Streamlit
    ↓
POST /upload
    ↓
FastAPI
2. OCR

PaddleOCR processes the uploaded document.

Document Image
      ↓
PaddleOCR
      ↓
Detected Text
      +
Bounding Boxes

The backend stores both the OCR text and its coordinates.

3. Document Detection

The OCR text is analyzed to identify the document type.

OCR Text
    ↓
Document Detector
    ↓
PAN / Aadhaar / Passport / Unknown
4. Document-Specific Extraction

For known document types, dedicated Python extractors are used.

PAN
 ↓
pan_extractor.py
Aadhaar
 ↓
aadhaar_extractor.py
Passport
 ↓
passport_extractor.py
5. Structured Data

The extracted information is converted into structured JSON.

Unstructured OCR Text
          ↓
    Extraction Logic
          ↓
    Structured JSON
6. Document Context

After processing, the backend temporarily keeps the current document context.

The context contains:

Document Type
Structured Data
OCR Text
OCR Bounding Boxes
Filename

This context is used by the Document Q&A system.

7. AI Question Answering

When the user asks a question:

User Question
      ↓
FastAPI /ask
      ↓
Groq AI
      ↓
Document Context
      ↓
AI Answer
8. Bounding Box Matching

After receiving the AI answer, the backend searches the OCR data for matching information.

AI Answer
    ↓
OCR Matching
    ↓
Matching OCR Text
    ↓
Bounding Box
    ↓
Streamlit
    ↓
Highlighted Document
🔌 API Endpoints
GET /

Checks whether the FastAPI backend is running.

Example Response
{
    "message": "AI Document Extractor API is running 🚀"
}
POST /upload

Uploads and processes a document.

Processing
Upload
  ↓
OCR
  ↓
Document Detection
  ↓
Information Extraction
  ↓
Structured JSON
Example Response
{
    "filename": "document.jpg",
    "document_type": "PAN Card",
    "data": {
        "pan_number": "XXXXXXXXXX",
        "name": "Example Name",
        "father_name": "Example Father",
        "date_of_birth": "DD/MM/YYYY"
    },
    "extracted_text": [],
    "ocr_data": []
}
POST /ask

Ask a question about the currently uploaded document.

Example
POST /ask?question=What%20is%20the%20date%20of%20birth?
Example Response
{
    "question": "What is the date of birth?",
    "answer": "The date of birth is DD/MM/YYYY.",
    "bounding_boxes": [
        {
            "text": "DD/MM/YYYY",
            "box": [100, 200, 250, 230]
        }
    ]
}
⚙️ Installation
1. Clone the Repository
git clone https://github.com/vedantjain-02/AI_Document_Extractor.git
cd AI_Document_Extractor
🐍 Backend Setup

Go to the backend directory:

cd backend

Create a virtual environment:

python -m venv .venv
Activate Virtual Environment
Windows PowerShell
.venv\Scripts\Activate.ps1
Install Dependencies
pip install -r requirements.txt
🔐 Environment Variables

Create a .env file inside the backend directory:

GROQ_API_KEY=your_groq_api_key_here
⚠️ Important

Never commit your real API key to GitHub.

Your .gitignore should contain:

.env
.venv/
__pycache__/
uploads/
▶️ Run Backend

From the backend directory:

uvicorn main:app --reload

The backend will run at:

http://127.0.0.1:8000
📚 Swagger API Documentation

FastAPI automatically provides interactive API documentation.

Open:

http://127.0.0.1:8000/docs

From Swagger, you can test:

GET /
POST /upload
POST /ask
🎨 Run Frontend

Open another terminal.

Go to the frontend:

cd frontend

Run Streamlit:

streamlit run app.py

The frontend will normally open at:

http://localhost:8501
🖥️ Application Interface

The frontend provides a dark-themed interface containing:

┌───────────────────────────────────────────────┐
│        📄 AI Document Extractor              │
│                                               │
│  Upload Document                              │
│  ┌─────────────────────────────────────────┐  │
│  │          Choose Document                │  │
│  └─────────────────────────────────────────┘  │
│                                               │
│  🔍 Analyze Document                          │
│                                               │
│  ⚙️ AI Processing Pipeline                    │
│                                               │
│  ┌──────────────────┐ ┌────────────────────┐ │
│  │ 📑 Document      │ │ 🧠 Extracted      │ │
│  │    Preview       │ │    Information     │ │
│  │                  │ │                    │ │
│  │   Document       │ │  Field → Value    │ │
│  │   Image          │ │                    │ │
│  │                  │ │                    │ │
│  └──────────────────┘ └────────────────────┘ │
│                                               │
│  🔎 Raw OCR Text                              │
│                                               │
│  📦 Structured JSON                           │
│                                               │
│                                  💬 Chat      │
└───────────────────────────────────────────────┘
🧪 Testing
Backend Health Check

Open:

http://127.0.0.1:8000/

Expected response:

{
    "message": "AI Document Extractor API is running 🚀"
}
Swagger

Open:

http://127.0.0.1:8000/docs
Frontend

Open:

http://localhost:8501
📊 Current Feature Status
Feature	Status
Document Upload	✅
PaddleOCR	✅
Bounding Box Extraction	✅
PAN Detection	✅
Aadhaar Detection	✅
Passport Detection	✅
PAN Extraction	✅
Aadhaar Extraction	✅
Passport Extraction	✅
Structured JSON	✅
Document Preview	✅
Raw OCR Display	✅
JSON Download	✅
Groq AI Integration	✅
Document Q&A	✅
Floating AI Chat	✅
Answer-to-OCR Matching	✅
Bounding Box Highlighting	✅
Multi-user Production Storage	🚧

⚠️ Current Limitations
This project is currently designed as a local prototype and portfolio project.

Current limitations include:

Document context is temporarily stored in backend memory.
The current implementation focuses on the latest uploaded document.
Multi-user session isolation is not implemented.
Production-grade document storage is not implemented.
PDF processing can require additional page-level handling.
OCR accuracy depends on document image quality.
Bounding-box matching can be improved for more complex questions.
🚧 Future Improvements

Planned improvements include:

✨ AI-powered OCR text cleanup
📑 Support for more document types
🚗 Better driving-license extraction
🌐 Multilingual document support
🎯 OCR confidence scores
🔎 Improved document-type detection
🧩 More robust field extraction
🎯 Improved field-to-OCR mapping
📄 Advanced PDF page processing
📊 Document processing history
👤 User authentication
🗃️ Database integration
☁️ Cloud deployment
🐳 Docker support
🔐 Production-grade security
⚡ Async/background document processing
🔒 Security & Privacy

This application may process sensitive identity documents.

For development and testing:

Never expose API keys.
Never commit .env files.
Avoid committing uploaded documents.
Do not log sensitive document numbers.
Use dummy or redacted documents for public demonstrations.

For production deployment, additional security measures should be implemented:

HTTPS
Authentication
Authorization
Secure file storage
Encryption
User/session isolation
API rate limiting
Data retention policies
Automatic deletion of temporary documents
Secure logging and monitoring
🎯 Project Goal

The goal of this project is to build a general-purpose AI Document Extraction system that can convert unstructured document images into structured and machine-readable information.

The project combines:

Computer Vision
       +
OCR
       +
Document Detection
       +
Information Extraction
       +
LLM
       +
FastAPI
       +
Streamlit

into a single end-to-end AI application.

💡 Key Learning Outcomes

This project demonstrates practical implementation of:

Optical Character Recognition
Computer Vision fundamentals
Text detection and recognition
Bounding-box processing
Document classification
Pattern-based information extraction
Structured JSON generation
LLM-powered question answering
Prompt engineering
FastAPI REST API development
Streamlit application development
Frontend-backend communication
Environment variable management
AI application architecture

👨‍💻 Author
Vedant Jain
AI / Python Developer

Interested in:
Python Backend Development
FastAPI
Artificial Intelligence
Computer Vision
OCR
LLM Applications


⭐ Project
If you find this project useful, consider giving the repository a ⭐.

📜 License
This project is licensed under the MIT License.
See the LICENSE file for more information.