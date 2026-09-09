import os
import json
import paddle

# =========================================================
# PADDLEPADDLE CONFIGURATION
# =========================================================

# Disable MKL-DNN because of PaddlePaddle CPU/PIR compatibility
# issues that can occur with some PaddleOCR versions.
os.environ["FLAGS_use_mkldnn"] = "0"

paddle.set_flags({
    "FLAGS_use_mkldnn": False
})


# =========================================================
# PADDLE OCR
# =========================================================

from paddleocr import PaddleOCR


ocr = PaddleOCR(
    lang="en",
    device="cpu",
    enable_mkldnn=False,
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False
)


# =========================================================
# OCR EXTRACTION
# =========================================================

def extract_text(image_path: str):
    """
    Run PaddleOCR and return OCR text along with
    bounding box coordinates.

    Example output:

    [
        {
            "text": "REPUBLIC OF INDIA",
            "box": [10, 20, 200, 50]
        },
        {
            "text": "PASSPORT",
            "box": [50, 70, 150, 100]
        }
    ]
    """

    result = ocr.predict(image_path)

    ocr_data = []

    for res in result:

        # PaddleOCR may return JSON string or dictionary
        data = res.json

        if isinstance(data, str):
            data = json.loads(data)

        # Some PaddleOCR responses contain data inside "res"
        if isinstance(data, dict) and "res" in data:
            data = data["res"]

        if not isinstance(data, dict):
            continue

        # OCR detected text
        rec_texts = data.get(
            "rec_texts",
            []
        )

        # OCR bounding boxes
        rec_boxes = data.get(
            "rec_boxes",
            []
        )

        # Fallback for polygon coordinates
        if not rec_boxes:
            rec_boxes = data.get(
                "rec_polys",
                []
            )

        # -------------------------------------------------
        # TEXT + BOX
        # -------------------------------------------------

        for index, text in enumerate(rec_texts):

            if not text:
                continue

            text = str(text).strip()

            if not text:
                continue

            box = None

            # Get corresponding bounding box
            if index < len(rec_boxes):

                raw_box = rec_boxes[index]

                try:

                    # NumPy array
                    if hasattr(raw_box, "tolist"):
                        box = raw_box.tolist()

                    else:
                        box = list(raw_box)

                except Exception:
                    box = None

            ocr_data.append({
                "text": text,
                "box": box
            })

    return ocr_data


# =========================================================
# GET ONLY TEXT
# =========================================================

def get_text_from_ocr_data(ocr_data):
    """
    Convert OCR data into a simple list of strings.

    Input:

    [
        {
            "text": "PASSPORT",
            "box": [...]
        },
        {
            "text": "REPUBLIC OF INDIA",
            "box": [...]
        }
    ]

    Output:

    [
        "PASSPORT",
        "REPUBLIC OF INDIA"
    ]

    This list is used by document detection
    and document-specific extractors.
    """

    texts = []

    for item in ocr_data:

        if not isinstance(item, dict):
            continue

        text = item.get("text")

        if text and str(text).strip():

            texts.append(
                str(text).strip()
            )

    return texts


# =========================================================
# GET OCR DATA WITHOUT EMPTY VALUES
# =========================================================

def clean_ocr_data(ocr_data):
    """
    Remove invalid OCR entries while keeping
    text + bounding box information.
    """

    cleaned_data = []

    for item in ocr_data:

        if not isinstance(item, dict):
            continue

        text = item.get("text")
        box = item.get("box")

        if not text:
            continue

        text = str(text).strip()

        if not text:
            continue

        cleaned_data.append({
            "text": text,
            "box": box
        })

    return cleaned_data