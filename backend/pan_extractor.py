import re


def find_next_value(texts, label_patterns):
    for i, text in enumerate(texts):
        text_lower = text.lower()

        for pattern in label_patterns:
            if re.search(pattern, text_lower):
                
                if i + 1 < len(texts):
                    value = texts[i + 1].strip()

                    if value:
                        return value

    return None


def extract_pan_details(extracted_text):

    # -----------------------------
    # PAN NUMBER
    # -----------------------------
    pan_number = None

    pan_pattern = r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"

    for text in extracted_text:
        match = re.search(pan_pattern, text.upper())

        if match:
            pan_number = match.group()
            break

    # -----------------------------
    # DATE OF BIRTH
    # -----------------------------
    date_of_birth = None

    dob_pattern = r"\b\d{2}[/-]\d{2}[/-]\d{4}\b"
    for text in extracted_text:
        match = re.search(dob_pattern, text)

        if match:
            date_of_birth = match.group()
            break

    # -----------------------------
    # NAME
    # -----------------------------
    name = find_next_value(
        extracted_text,
        [
            r"/name",
            r"\bname\b"
        ]
    )

    # -----------------------------
    # FATHER'S NAME
    # -----------------------------
    father_name = find_next_value(
        extracted_text,
        [
            r"father.?s name",
            r"father",
            r"fathers name"
        ]
    )

    return {
        "pan_number": pan_number,
        "name": name,
        "father_name": father_name,
        "date_of_birth": date_of_birth
    }