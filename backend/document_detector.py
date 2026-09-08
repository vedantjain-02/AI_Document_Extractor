import re


def detect_document_type(texts):

    text = " ".join(texts).lower()

    # PAN Card
    pan_pattern = r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"

    if (
        "income tax department" in text
        or "permanent account number" in text
        or re.search(pan_pattern, text.upper())
    ):
        return "PAN Card"

    # Aadhaar
    if (
        "aadhaar" in text
        or "unique identification authority of india" in text
        or "uidai" in text
    ):
        return "Aadhaar Card"

    # Passport
    if (
        "passport" in text
        or "republic of india" in text
    ):
        return "Passport"

    return "Unknown"