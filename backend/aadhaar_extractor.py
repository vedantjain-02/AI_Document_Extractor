import re


def extract_aadhaar_details(texts):

    aadhaar_number = None
    name = None
    date_of_birth = None
    year_of_birth = None
    gender = None

    # --------------------------------
    # AADHAAR NUMBER
    # --------------------------------
    aadhaar_pattern = r"\b\d{4}\s?\d{4}\s?\d{4}\b"

    for text in texts:
        match = re.search(aadhaar_pattern, text)

        if match:
            aadhaar_number = re.sub(
                r"\s+",
                " ",
                match.group()
            )
            break

    # --------------------------------
    # DATE OF BIRTH
    # --------------------------------
    dob_pattern = r"\b\d{2}[/-]\d{2}[/-]\d{4}\b"

    dob_index = None

    for i, text in enumerate(texts):

        match = re.search(dob_pattern, text)

        if match:
            date_of_birth = match.group()
            dob_index = i
            break

    # --------------------------------
    # YEAR OF BIRTH
    # --------------------------------

    if date_of_birth:
        year_of_birth = date_of_birth[-4:]

    else:
        yob_pattern = r"\b(?:19|20)\d{2}\b"

        for i, text in enumerate(texts):

            if (
                "year of birth" in text.lower()
                or "yob" in text.lower()
            ):
                match = re.search(yob_pattern, text)

                if match:
                    year_of_birth = match.group()
                    break
    # --------------------------------
    # GENDER
    # --------------------------------
    for text in texts:

        value = text.strip().lower()

        if value in ["male", "पुरुष"]:
            gender = "Male"
            break

        elif value in ["female", "महिला"]:
            gender = "Female"
            break

    # --------------------------------
    # NAME
    # --------------------------------

    if dob_index is not None:

        for i in range(dob_index - 1, max(-1, dob_index - 4), -1):

            value = texts[i].strip()

            if not value:
                continue

            # Skip obvious labels/noise
            lower_value = value.lower()

            if any(
                keyword in lower_value
                for keyword in [
                    "dob",
                    "date of birth",
                    "year of birth",
                    "gender",
                    "male",
                    "female",
                    "aadhaar",
                    "government",
                    "india"
                ]
            ):
                continue

            # Skip numbers
            if re.fullmatch(r"[\d\s/-]+", value):
                continue

            # Name should contain letters
            if re.fullmatch(r"[A-Za-z .'-]+", value):

                # Avoid very short OCR noise
                if len(value) >= 3:
                    name = value
                    break

    return {
        "aadhaar_number": aadhaar_number,
        "name": name,
        "date_of_birth": date_of_birth,
        "year_of_birth": year_of_birth,
        "gender": gender
    }