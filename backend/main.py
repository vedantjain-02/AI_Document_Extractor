import os
import re

from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel

from ocr_service import (
    extract_text,
    get_text_from_ocr_data
)

from extractor_router import extract_document_data
from document_detector import detect_document_type
from grok_service import ask_document_question


# =========================================================
# FASTAPI CONFIGURATION
# =========================================================

app = FastAPI(
    title="AI Document Extractor",
    description="Document Information Extraction API",
    version="1.0.0"
)


# =========================================================
# QUESTION REQUEST MODEL
# =========================================================

class QuestionRequest(BaseModel):

    question: str

    document_type: str

    document_data: dict

    extracted_text: list


# =========================================================
# DOCUMENT CONTEXT
# =========================================================

document_context = {

    "document_type": None,

    "document_data": None,

    "extracted_text": None,

    "ocr_data": None,

    "filename": None
}


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():

    return {
        "message": "AI Document Extractor API is running 🚀"
    }


# =========================================================
# FIND MATCHING OCR BOXES
# =========================================================

def find_matching_boxes(
    answer,
    ocr_data,
    document_data
):
    """
    Find OCR bounding boxes that correspond
    to the AI answer.

    This allows the frontend to highlight
    the relevant information on the document.
    """

    if not answer or not ocr_data:

        return []

    answer_text = str(answer).strip()

    if not answer_text:

        return []

    matches = []

    # -----------------------------------------------------
    # NORMALIZE TEXT
    # -----------------------------------------------------

    def normalize(text):

        if text is None:
            return ""

        text = str(text).lower()

        text = re.sub(
            r"[^a-z0-9]+",
            " ",
            text
        )

        return " ".join(
            text.split()
        )

    normalized_answer = normalize(
        answer_text
    )

    # =====================================================
    # 1. EXACT OCR TEXT MATCH
    # =====================================================

    for item in ocr_data:

        ocr_text = item.get(
            "text",
            ""
        )

        box = item.get(
            "box"
        )

        if not ocr_text or not box:
            continue

        normalized_ocr = normalize(
            ocr_text
        )

        if not normalized_ocr:
            continue

        if (
            normalized_ocr == normalized_answer
            or normalized_ocr in normalized_answer
            or normalized_answer in normalized_ocr
        ):

            matches.append({
                "text": ocr_text,
                "box": box
            })

    if matches:

        return matches


    # =====================================================
    # 2. STRUCTURED DATA MATCH
    # =====================================================

    if isinstance(
        document_data,
        dict
    ):

        values_to_find = []

        for value in document_data.values():

            if value is None:
                continue

            if isinstance(
                value,
                (dict, list)
            ):
                continue

            value = str(
                value
            ).strip()

            if value:

                values_to_find.append(
                    value
                )


        for value in values_to_find:

            normalized_value = normalize(
                value
            )

            if not normalized_value:
                continue


            if (
                normalized_value in normalized_answer
                or normalized_answer in normalized_value
            ):

                for item in ocr_data:

                    ocr_text = item.get(
                        "text",
                        ""
                    )

                    box = item.get(
                        "box"
                    )

                    if not ocr_text or not box:
                        continue

                    normalized_ocr = normalize(
                        ocr_text
                    )


                    if (
                        normalized_ocr == normalized_value
                        or normalized_value in normalized_ocr
                        or normalized_ocr in normalized_value
                    ):

                        matches.append({
                            "text": ocr_text,
                            "box": box
                        })


        if matches:

            return matches


    # =====================================================
    # 3. WORD LEVEL MATCH
    # =====================================================

    answer_words = normalized_answer.split()

    answer_words = [

        word

        for word in answer_words

        if len(word) >= 3

    ]


    for word in answer_words:

        for item in ocr_data:

            ocr_text = item.get(
                "text",
                ""
            )

            box = item.get(
                "box"
            )

            if not ocr_text or not box:
                continue

            normalized_ocr = normalize(
                ocr_text
            )


            if (
                normalized_ocr == word
                or word in normalized_ocr
            ):

                matches.append({
                    "text": ocr_text,
                    "box": box
                })


    # =====================================================
    # REMOVE DUPLICATES
    # =====================================================

    unique_matches = []

    seen = set()


    for match in matches:

        key = (
            str(
                match.get("text")
            ),

            str(
                match.get("box")
            )
        )


        if key not in seen:

            seen.add(key)

            unique_matches.append(
                match
            )


    return unique_matches


# =========================================================
# UPLOAD DOCUMENT
# =========================================================

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    # -----------------------------------------------------
    # CREATE UPLOAD DIRECTORY
    # -----------------------------------------------------

    os.makedirs(
        "uploads",
        exist_ok=True
    )


    # -----------------------------------------------------
    # SAVE FILE
    # -----------------------------------------------------

    file_path = os.path.join(
        "uploads",
        file.filename
    )


    with open(
        file_path,
        "wb"
    ) as buffer:

        buffer.write(
            await file.read()
        )


    # =====================================================
    # OCR
    # =====================================================

    # OCR now returns:
    #
    # [
    #     {
    #         "text": "...",
    #         "box": [...]
    #     }
    # ]

    ocr_data = extract_text(
        file_path
    )


    # =====================================================
    # EXTRACT ONLY TEXT
    # =====================================================

    extracted_text = get_text_from_ocr_data(
        ocr_data
    )


    # =====================================================
    # DOCUMENT TYPE DETECTION
    # =====================================================

    document_type = detect_document_type(
        extracted_text
    )


    # =====================================================
    # DOCUMENT DATA EXTRACTION
    # =====================================================

    document_data = extract_document_data(
        document_type,
        extracted_text
    )


    # =====================================================
    # HANDLE GENERIC EXTRACTOR RESPONSE
    # =====================================================

    if (
        document_type == "Unknown"
        and isinstance(
            document_data,
            dict
        )
    ):

        document_type = document_data.get(
            "document_type",
            "Unknown"
        )


    # =====================================================
    # STRUCTURED DATA
    # =====================================================

    if isinstance(
        document_data,
        dict
    ):

        structured_data = document_data.get(
            "data",
            document_data
        )

    else:

        structured_data = document_data


    # =====================================================
    # SAVE DOCUMENT CONTEXT
    # =====================================================

    document_context[
        "document_type"
    ] = document_type


    document_context[
        "document_data"
    ] = structured_data


    document_context[
        "extracted_text"
    ] = extracted_text


    document_context[
        "ocr_data"
    ] = ocr_data


    document_context[
        "filename"
    ] = file.filename


    # =====================================================
    # RESPONSE
    # =====================================================

    return {

        "filename": file.filename,

        "document_type": document_type,

        "data": structured_data,

        "extracted_text": extracted_text,

        "ocr_data": ocr_data

    }


# =========================================================
# DOCUMENT QUESTION / AI CHAT
# =========================================================

@app.post("/ask")
async def ask_question(
    question: str
):

    # -----------------------------------------------------
    # CHECK DOCUMENT
    # -----------------------------------------------------

    if (
        document_context[
            "document_type"
        ] is None
    ):

        return {

            "error":
                "Please upload a document first."

        }


    # =====================================================
    # ASK GROQ AI
    # =====================================================

    answer = ask_document_question(

        question=question,

        document_type=(
            document_context[
                "document_type"
            ]
        ),

        document_data=(
            document_context[
                "document_data"
            ]
        ),

        extracted_text=(
            document_context[
                "extracted_text"
            ]
        )

    )


    # =====================================================
    # FIND RELEVANT BOUNDING BOXES
    # =====================================================

    bounding_boxes = find_matching_boxes(

        answer=answer,

        ocr_data=(
            document_context[
                "ocr_data"
            ]
        ),

        document_data=(
            document_context[
                "document_data"
            ]
        )

    )


    # =====================================================
    # RESPONSE
    # =====================================================

    return {

        "question": question,

        "answer": answer,

        "bounding_boxes": bounding_boxes

    }