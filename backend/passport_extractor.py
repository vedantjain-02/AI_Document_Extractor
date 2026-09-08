import re


def extract_passport_details(texts):

    passport_number = None
    surname = None
    given_name = None
    date_of_birth = None
    nationality = None
    sex = None

    # --------------------------------
    # PASSPORT NUMBER
    # --------------------------------
    passport_pattern = r"\b[A-Z]{1,2}[0-9]{6,7}\b"

    for text in texts:
        match = re.search(passport_pattern, text.upper())

        if match:
            passport_number = match.group()
            break

    # --------------------------------
    # NATIONALITY
    # --------------------------------
    # Look for a 3-letter country code near "Code"
    for i, text in enumerate(texts):

        if "code" in text.lower():

            for j in range(i + 1, min(i + 4, len(texts))):

                value = texts[j].strip().upper()

                if re.fullmatch(r"[A-Z]{3}", value):
                    nationality = value
                    break

            if nationality:
                break

    # --------------------------------
    # DATE OF BIRTH
    # --------------------------------
    dob_pattern = r"\b\d{2}/\d{2}/\d{4}\b"

    for text in texts:

        match = re.search(dob_pattern, text)

        if match:
            date_of_birth = match.group()
            break

    # --------------------------------
    # SURNAME
    # --------------------------------
    for i, text in enumerate(texts):

        cleaned = text.lower()

        # OCR may read "Surname" incorrectly
        if "surname" in cleaned or "sumame" in cleaned:

            if i + 1 < len(texts):
                value = texts[i + 1].strip()

                if value:
                    surname = value

            break

    # --------------------------------
    # GIVEN NAME
    # --------------------------------
    for i, text in enumerate(texts):

        cleaned = text.lower()

        # OCR may read "Given Name" as "Give"
        if "given" in cleaned or cleaned.strip() in ["/ give", "give"]:

            if i + 1 < len(texts):
                value = texts[i + 1].strip()

                if value:
                    given_name = value

            break

    # --------------------------------
    # FULL NAME
    # --------------------------------
    name = None

    if given_name and surname:
        name = f"{given_name} {surname}"

    elif given_name:
        name = given_name

    elif surname:
        name = surname

    # --------------------------------
    # SEX
    # --------------------------------
    for text in texts:

        value = text.strip().upper()

        if value in ["M", "F"]:
            sex = value
            break

    # --------------------------------
    # RETURN DATA
    # --------------------------------
    return {
        "passport_number": passport_number,
        "name": name,
        "date_of_birth": date_of_birth,
        "nationality": nationality,
        "sex": sex
    }