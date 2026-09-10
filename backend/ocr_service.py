import os
import json
import tempfile

import paddle
from PIL import Image


# =========================================================
# PADDLE CPU CONFIG
# =========================================================

os.environ["FLAGS_use_mkldnn"] = "0"

paddle.set_flags({
    "FLAGS_use_mkldnn": False
})


from paddleocr import PaddleOCR


# =========================================================
# OCR CONFIG
# =========================================================

ocr = PaddleOCR(
    # =====================================================
    # LIGHTWEIGHT OCR MODELS
    # =====================================================

    text_detection_model_name="PP-OCRv5_mobile_det",
    text_recognition_model_name="PP-OCRv5_mobile_rec",

    # =====================================================
    # CPU
    # =====================================================

    device="cpu",

    # Earlier PaddlePaddle CPU issue workaround
    enable_mkldnn=False,

    # =====================================================
    # Disable unnecessary processing
    # =====================================================

    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False,

    # =====================================================
    # Detection optimization
    # =====================================================

    text_det_limit_side_len=768,
    text_det_limit_type="max",

    # =====================================================
    # Recognition
    # =====================================================

    text_rec_score_thresh=0.2
)

# =========================================================
# IMAGE SIZE OPTIMIZATION
# =========================================================

MAX_IMAGE_SIDE = 1200


def prepare_image_for_ocr(image_path):

    image = Image.open(
        image_path
    ).convert("RGB")

    original_width, original_height = image.size

    max_side = max(
        original_width,
        original_height
    )

    # -----------------------------------------------------
    # No resize required
    # -----------------------------------------------------

    if max_side <= MAX_IMAGE_SIDE:

        return (
            image_path,
            1.0,
            1.0,
            None
        )

    # -----------------------------------------------------
    # Calculate resize ratio
    # -----------------------------------------------------

    scale = (
        MAX_IMAGE_SIDE / max_side
    )

    new_width = int(
        original_width * scale
    )

    new_height = int(
        original_height * scale
    )

    resized_image = image.resize(
        (
            new_width,
            new_height
        ),
        Image.Resampling.LANCZOS
    )

    # -----------------------------------------------------
    # Temporary file
    # -----------------------------------------------------

    temp_file = tempfile.NamedTemporaryFile(
        suffix=".jpg",
        delete=False
    )

    temp_path = temp_file.name

    temp_file.close()

    resized_image.save(
        temp_path,
        quality=90
    )

    # -----------------------------------------------------
    # Scale factors
    # -----------------------------------------------------

    scale_x = (
        original_width / new_width
    )

    scale_y = (
        original_height / new_height
    )

    return (
        temp_path,
        scale_x,
        scale_y,
        temp_path
    )


# =========================================================
# SCALE OCR BOX
# =========================================================

def scale_box(
    box,
    scale_x,
    scale_y
):

    if not box:
        return box

    try:

        # -------------------------------------------------
        # Rectangle
        # [x1, y1, x2, y2]
        # -------------------------------------------------

        if (
            len(box) == 4
            and all(
                isinstance(
                    value,
                    (int, float)
                )
                for value in box
            )
        ):

            return [
                int(box[0] * scale_x),
                int(box[1] * scale_y),
                int(box[2] * scale_x),
                int(box[3] * scale_y)
            ]

        # -------------------------------------------------
        # Polygon
        # [[x1,y1], [x2,y2], ...]
        # -------------------------------------------------

        if (
            len(box) >= 3
            and isinstance(
                box[0],
                (list, tuple)
            )
        ):

            scaled_points = []

            for point in box:

                if (
                    isinstance(
                        point,
                        (list, tuple)
                    )
                    and len(point) >= 2
                ):

                    scaled_points.append(
                        [
                            int(
                                point[0] * scale_x
                            ),
                            int(
                                point[1] * scale_y
                            )
                        ]
                    )

            return scaled_points

    except Exception:

        return box

    return box


# =========================================================
# OCR EXTRACTION
# =========================================================

def extract_text(image_path: str):

    ocr_path = image_path

    scale_x = 1.0
    scale_y = 1.0

    temp_path = None

    # =====================================================
    # PREPARE IMAGE
    # =====================================================

    try:

        (
            ocr_path,
            scale_x,
            scale_y,
            temp_path
        ) = prepare_image_for_ocr(
            image_path
        )

    except Exception:

        ocr_path = image_path

        scale_x = 1.0
        scale_y = 1.0

        temp_path = None

    try:

        # =================================================
        # RUN OCR
        # =================================================

        result = ocr.predict(
            ocr_path
        )

        ocr_data = []

        # =================================================
        # PROCESS OCR RESULT
        # =================================================

        for res in result:

            data = res.json

            if isinstance(
                data,
                str
            ):

                data = json.loads(
                    data
                )

            if (
                isinstance(
                    data,
                    dict
                )
                and "res" in data
            ):

                data = data["res"]

            if not isinstance(
                data,
                dict
            ):

                continue

            rec_texts = data.get(
                "rec_texts",
                []
            )

            rec_boxes = data.get(
                "rec_boxes",
                []
            )

            if not rec_boxes:

                rec_boxes = data.get(
                    "rec_polys",
                    []
                )

            # =================================================
            # BUILD OCR DATA
            # =================================================

            for index, text in enumerate(
                rec_texts
            ):

                if not text:
                    continue

                text = str(
                    text
                ).strip()

                if not text:
                    continue

                box = None

                # -------------------------------------------------
                # Get corresponding box
                # -------------------------------------------------

                if index < len(
                    rec_boxes
                ):

                    raw_box = rec_boxes[
                        index
                    ]

                    try:

                        if hasattr(
                            raw_box,
                            "tolist"
                        ):

                            box = raw_box.tolist()

                        else:

                            box = list(
                                raw_box
                            )

                    except Exception:

                        box = None

                # -------------------------------------------------
                # Convert resized coordinates
                # back to original image
                # -------------------------------------------------

                if box:

                    box = scale_box(
                        box,
                        scale_x,
                        scale_y
                    )

                ocr_data.append(
                    {
                        "text": text,
                        "box": box
                    }
                )

        return ocr_data

    finally:

        # =================================================
        # DELETE TEMP IMAGE
        # =================================================

        if temp_path:

            try:

                os.remove(
                    temp_path
                )

            except Exception:

                pass


# =========================================================
# GET TEXT ONLY
# =========================================================

def get_text_from_ocr_data(
    ocr_data
):

    texts = []

    for item in ocr_data:

        if not isinstance(
            item,
            dict
        ):
            continue

        text = item.get(
            "text"
        )

        if text and str(
            text
        ).strip():

            texts.append(
                str(
                    text
                ).strip()
            )

    return texts


# =========================================================
# CLEAN OCR DATA
# =========================================================

def clean_ocr_data(
    ocr_data
):

    cleaned_data = []

    for item in ocr_data:

        if not isinstance(
            item,
            dict
        ):
            continue

        text = item.get(
            "text"
        )

        box = item.get(
            "box"
        )

        if not text:
            continue

        text = str(
            text
        ).strip()

        if not text:
            continue

        cleaned_data.append(
            {
                "text": text,
                "box": box
            }
        )

    return cleaned_data