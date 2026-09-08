import os
import json
import paddle

os.environ["FLAGS_use_mkldnn"] = "0"


paddle.set_flags({
    "FLAGS_use_mkldnn": False
})

from paddleocr import PaddleOCR

ocr = PaddleOCR(
    lang="en",
    device="cpu",
    enable_mkldnn=False,
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False
)


def extract_text(image_path: str):
    result = ocr.predict(image_path)

    texts = []

    for res in result:
        data = res.json

        if isinstance(data, str):
            data = json.loads(data)

        if isinstance(data, dict) and "res" in data:
            data = data["res"]

        if isinstance(data, dict):
            rec_texts = data.get("rec_texts", [])

            for text in rec_texts:
                if text and text.strip():
                    texts.append(text.strip())

    return texts