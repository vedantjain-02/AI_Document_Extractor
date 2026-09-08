from pan_extractor import extract_pan_details
from passport_extractor import extract_passport_details
from aadhaar_extractor import extract_aadhaar_details
from generic_extractor import extract_generic_document

def extract_document_data(document_type, extracted_text):

    if document_type == "PAN Card":
        return extract_pan_details(extracted_text)

    elif document_type == "Passport":
        return extract_passport_details(extracted_text)

    elif document_type == "Aadhaar Card":
        return extract_aadhaar_details(extracted_text)

    else:
        return extract_generic_document(extracted_text)