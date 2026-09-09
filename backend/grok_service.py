import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"
)


def ask_document_question(question, document_type, document_data, extracted_text):
    context = f"""
    Document Type:
    {document_type}

    Structured Document Data:
    {document_data}

    OCR Text:
    {extracted_text}
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": """
You are an AI document assistant.

Answer the user's question only using the information available
in the provided document context.

Rules:
- Do not invent information.
- If the requested information is not present, say:
  "I couldn't find that information in the document."
- Give a short and direct answer.
- Preserve names, numbers and dates exactly as provided.
"""
            },
            {
                "role": "user",
                "content": f"""
{context}

Question:
{question}
"""
            }
        ]
    )

    return response.choices[0].message.content
