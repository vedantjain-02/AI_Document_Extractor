import json
from grok_service import client


def extract_generic_document(texts):

    ocr_text = "\n".join(texts)

    prompt = f"""
You are an intelligent document information extraction system.

Analyze the OCR text below and extract information from the document.

Rules:
1. Identify the document type yourself.
2. Do NOT invent any information.
3. Extract only information explicitly present in the OCR text.
4. If a useful field is not available, use null.
5. Use meaningful field names based on the actual document.
6. Return ONLY valid JSON.
7. Do not add markdown or explanations.
8. Do not calculate, infer, or guess values such as age.
9. Preserve extracted values accurately from the OCR text.
10. Do not include fields whose values are not supported by the OCR text.

OCR TEXT:
{ocr_text}

Return exactly this structure:

{{
    "document_type": "identified document type",
    "data": {{
        "field_name": "value"
    }}
}}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    result = response.choices[0].message.content

    try:
        parsed = json.loads(result)

        return {
            "document_type": parsed.get("document_type"),
            "data": parsed.get("data", {})
        }

    except json.JSONDecodeError:
        return {
            "document_type": "Unknown",
            "data": {},
            "raw_response": result
        }