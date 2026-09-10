import json
import base64
from io import BytesIO

import requests
import streamlit as st
from PIL import Image, ImageDraw


# =========================================================
# CONFIG
# =========================================================

BACKEND_URL = "http://127.0.0.1:8000"


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Document Extractor",
    page_icon="📄",
    layout="wide"
)


# =========================================================
# DARK THEME
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0e1117;
        color: white;
    }

    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        color: #9ca3af;
        font-size: 17px;
        margin-bottom: 30px;
    }

    .field-label {
        color: #9ca3af;
        font-size: 14px;
        margin-bottom: 2px;
    }

    .field-value {
        color: white;
        font-size: 17px;
        font-weight: 600;
        margin-bottom: 15px;
    }

    .chat-user {
        background-color: #1f2937;
        padding: 10px 14px;
        border-radius: 10px;
        margin-bottom: 8px;
    }

    .chat-ai {
        background-color: #111827;
        padding: 10px 14px;
        border-radius: 10px;
        margin-bottom: 15px;
        border: 1px solid #374151;
    }

    /* ================================================
    FLOATING CHAT BUTTON
    ================================================ */

    div[data-testid="stPopover"] {
        position: fixed !important;
        right: 24px !important;
        bottom: 24px !important;

        width: 60px !important;
        min-width: 60px !important;
        max-width: 60px !important;

        height: 60px !important;

        margin: 0 !important;
        padding: 0 !important;

        z-index: 999999 !important;
    }


    /* Chat Button */

    div[data-testid="stPopover"] > button {
        width: 60px !important;
        min-width: 60px !important;
        max-width: 60px !important;

        height: 60px !important;
        min-height: 60px !important;

        padding: 0 !important;
        margin: 0 !important;

        border-radius: 50% !important;

        font-size: 25px !important;

        border: 1px solid #374151 !important;

        background: #1f2937 !important;

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.45) !important;

        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }


    /* Hover */

    div[data-testid="stPopover"] > button:hover {
        border-color: #ff3030 !important;

        transform: scale(1.05) !important;

        transition: 0.2s ease !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "uploaded_file_data" not in st.session_state:
    st.session_state.uploaded_file_data = None

if "uploaded_file_name" not in st.session_state:
    st.session_state.uploaded_file_name = None

if "uploaded_file_type" not in st.session_state:
    st.session_state.uploaded_file_type = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "bounding_boxes" not in st.session_state:
    st.session_state.bounding_boxes = []


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">📄 AI Document Extractor</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Upload your document and extract information using AI</div>',
    unsafe_allow_html=True
)


# =========================================================
# UPLOAD SECTION
# =========================================================

uploaded_file = st.file_uploader(
    "Upload Document",
    type=[
        "png",
        "jpg",
        "jpeg",
        "webp",
        "pdf"
    ]
)


# =========================================================
# HANDLE NEW FILE
# =========================================================

if uploaded_file is not None:

    current_file_name = uploaded_file.name

    if (
        st.session_state.uploaded_file_name
        != current_file_name
    ):

        st.session_state.result = None

        st.session_state.chat_history = []

        st.session_state.bounding_boxes = []

        st.session_state.uploaded_file_data = (
            uploaded_file.getvalue()
        )

        st.session_state.uploaded_file_name = (
            uploaded_file.name
        )

        st.session_state.uploaded_file_type = (
            uploaded_file.type
        )


# =========================================================
# ANALYZE BUTTON
# =========================================================

if uploaded_file is not None:

    if st.button(
        "🔍 Analyze Document",
        use_container_width=True
    ):

        with st.spinner(
            "Analyzing document..."
        ):

            try:

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }

                response = requests.post(
                    f"{BACKEND_URL}/upload",
                    files=files,
                    timeout=120
                )

                if response.status_code == 200:

                    result = response.json()

                    st.session_state.result = result

                    st.session_state.bounding_boxes = []

                    st.success(
                        "Document analyzed successfully! ✅"
                    )

                    st.rerun()

                else:

                    st.error(
                        f"Backend Error: {response.text}"
                    )

            except Exception as e:

                st.error(
                    f"Could not connect to backend: {e}"
                )


# =========================================================
# RESULT SECTION
# =========================================================

result = st.session_state.result


if result:

    # =====================================================
    # PIPELINE
    # =====================================================

    st.markdown(
        "## 🔄 Processing Pipeline"
    )

    pipeline_columns = st.columns(5)

    pipeline_steps = [
        "📤 Upload",
        "🔍 OCR",
        "🧠 Detection",
        "📊 Extraction",
        "🤖 Q&A"
    ]

    for column, step in zip(
        pipeline_columns,
        pipeline_steps
    ):

        with column:

            st.info(step)


    # =====================================================
    # IMAGE PREVIEW
    # =====================================================

    file_data = (
        st.session_state.uploaded_file_data
    )

    file_type = (
        st.session_state.uploaded_file_type
    )


    if (
        file_data
        and file_type
        and file_type.startswith("image/")
    ):

        try:

            # -------------------------------------------------
            # ORIGINAL IMAGE
            # -------------------------------------------------

            original_image = Image.open(
                BytesIO(file_data)
            ).convert("RGB")


            # =================================================
            # IMAGE 1
            # ORIGINAL IMAGE + Q&A BOXES
            # =================================================

            qa_image = original_image.copy()

            qa_draw = ImageDraw.Draw(
                qa_image
            )


            # -------------------------------------------------
            # EXISTING Q&A BOUNDING BOXES
            # -------------------------------------------------

            for item in st.session_state.bounding_boxes:

                if not isinstance(
                    item,
                    dict
                ):
                    continue


                box = item.get(
                    "box"
                )

                if not box:
                    continue


                try:

                    # -----------------------------------------
                    # RECTANGLE
                    # [x1, y1, x2, y2]
                    # -----------------------------------------

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

                        x1, y1, x2, y2 = map(
                            int,
                            box
                        )

                        qa_draw.rectangle(
                            [
                                x1,
                                y1,
                                x2,
                                y2
                            ],
                            outline="#ff3030",
                            width=5
                        )


                    # -----------------------------------------
                    # POLYGON
                    # -----------------------------------------

                    elif (
                        len(box) >= 3
                        and isinstance(
                            box[0],
                            (list, tuple)
                        )
                    ):

                        points = []

                        for point in box:

                            if (
                                isinstance(
                                    point,
                                    (list, tuple)
                                )
                                and len(point) >= 2
                            ):

                                points.append(
                                    (
                                        int(point[0]),
                                        int(point[1])
                                    )
                                )


                        if len(points) >= 3:

                            qa_draw.line(
                                points + [points[0]],
                                fill="#ff3030",
                                width=5
                            )


                except Exception:

                    continue


            # =================================================
            # IMAGE 2
            # DUPLICATE IMAGE + ALL OCR BOXES
            # =================================================

            ocr_image = original_image.copy()

            ocr_draw = ImageDraw.Draw(
                ocr_image
            )


            # -------------------------------------------------
            # GET OCR DATA
            # -------------------------------------------------

            ocr_data = result.get(
                "ocr_data",
                []
            )

            ocr_box_count = 0


            # -------------------------------------------------
            # DRAW ALL OCR BOXES
            # -------------------------------------------------

            for item in ocr_data:

                if not isinstance(
                    item,
                    dict
                ):
                    continue


                box = item.get(
                    "box"
                )

                if not box:
                    continue


                try:

                    # -----------------------------------------
                    # RECTANGLE
                    # -----------------------------------------

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

                        x1, y1, x2, y2 = map(
                            int,
                            box
                        )

                        ocr_draw.rectangle(
                            [
                                x1,
                                y1,
                                x2,
                                y2
                            ],
                            outline="#ff3030",
                            width=2
                        )

                        ocr_box_count += 1


                    # -----------------------------------------
                    # POLYGON
                    # -----------------------------------------

                    elif (
                        len(box) >= 3
                        and isinstance(
                            box[0],
                            (list, tuple)
                        )
                    ):

                        points = []

                        for point in box:

                            if (
                                isinstance(
                                    point,
                                    (list, tuple)
                                )
                                and len(point) >= 2
                            ):

                                points.append(
                                    (
                                        int(point[0]),
                                        int(point[1])
                                    )
                                )


                        if len(points) >= 3:

                            ocr_draw.line(
                                points + [points[0]],
                                fill="#ff3030",
                                width=2
                            )

                            ocr_box_count += 1


                except Exception:

                    continue


            # =================================================
            # SIDE BY SIDE IMAGES
            # =================================================

            image_column_1, image_column_2 = st.columns(
                2,
                gap="medium"
            )


            # -------------------------------------------------
            # LEFT: ORIGINAL + Q&A BOX
            # -------------------------------------------------

            with image_column_1:

                st.markdown(
                    "### Original Document"
                )

                st.image(
                    qa_image,
                    use_container_width=True
                )


            # -------------------------------------------------
            # RIGHT: ALL OCR BOXES
            # -------------------------------------------------

            with image_column_2:

                st.markdown(
                    "### Text detected from the image"
                )

                st.image(
                    ocr_image,
                    use_container_width=True
                )


            # -------------------------------------------------
            # OCR COUNT
            # -------------------------------------------------

            if ocr_box_count > 0:

                st.success(
                    f"🔴 {ocr_box_count} OCR text region(s) detected"
                )

            else:

                st.info(
                    "No OCR bounding boxes were detected."
                )


        except Exception as e:

            st.error(
                f"Could not display image: {e}"
            )


    # =====================================================
    # DOCUMENT INFORMATION
    # =====================================================

    st.markdown(
        "## 📋 Extracted Information"
    )


    document_type = result.get(
        "document_type",
        "Unknown"
    )


    st.markdown(
        f"**Document Type:** `{document_type}`"
    )


    document_data = result.get(
        "data",
        {}
    )


    if isinstance(
        document_data,
        dict
    ):

        columns = st.columns(2)

        items = list(
            document_data.items()
        )

        for index, (
            key,
            value
        ) in enumerate(items):

            with columns[
                index % 2
            ]:

                st.markdown(
                    f"""
                    <div class="field-label">
                        {key.replace("_", " ").title()}
                    </div>

                    <div class="field-value">
                        {value if value else "Not Found"}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


    # =====================================================
    # RAW OCR
    # =====================================================

    with st.expander(
        "Raw OCR Text"
    ):

        extracted_text = result.get(
            "extracted_text",
            []
        )


        if isinstance(
            extracted_text,
            list
        ):

            st.text(
                "\n".join(
                    str(text)
                    for text in extracted_text
                )
            )

        else:

            st.text(
                str(extracted_text)
            )


    # =====================================================
    # STRUCTURED JSON
    # =====================================================

    with st.expander(
        "🧾 Structured JSON"
    ):

        st.json(
            document_data
        )


    # =====================================================
    # NEW DOCUMENT BUTTON
    # =====================================================

    if st.button(
        "📄 Analyze New Document",
        use_container_width=True
    ):

        st.session_state.result = None

        st.session_state.uploaded_file_data = None

        st.session_state.uploaded_file_name = None

        st.session_state.uploaded_file_type = None

        st.session_state.chat_history = []

        st.session_state.bounding_boxes = []

        st.rerun()


    # =====================================================
    # FLOATING DOCUMENT Q&A
    # =====================================================

    with st.popover("💬"):

        st.markdown(
            "### 🤖 Document Assistant"
        )

        st.caption(
            "Ask anything about your uploaded document"
        )


        # -------------------------------------------------
        # CHAT HISTORY
        # -------------------------------------------------

        for chat in st.session_state.chat_history:

            if chat["role"] == "user":

                st.markdown(
                    f"""
                    <div class="chat-user">
                        <b>You:</b> {chat["content"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"""
                    <div class="chat-ai">
                        <b>AI:</b> {chat["content"]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )


        # -------------------------------------------------
        # QUESTION INPUT
        # -------------------------------------------------

        question = st.text_input(
            "Ask a question",
            placeholder="e.g. What is the passport number?",
            key="document_question"
        )


        # -------------------------------------------------
        # SEND BUTTON
        # -------------------------------------------------

        if st.button(
            "Send",
            use_container_width=True
        ):

            if question.strip():

                user_question = question.strip()


                # -----------------------------------------
                # SAVE USER QUESTION
                # -----------------------------------------

                st.session_state.chat_history.append(
                    {
                        "role": "user",
                        "content": user_question
                    }
                )


                try:

                    with st.spinner(
                        "Thinking..."
                    ):

                        response = requests.post(
                            f"{BACKEND_URL}/ask",
                            params={
                                "question": user_question
                            },
                            timeout=120
                        )


                    if response.status_code == 200:

                        answer_data = response.json()


                        answer = answer_data.get(
                            "answer",
                            "I couldn't find that information in the document."
                        )


                        # ---------------------------------
                        # SAVE Q&A BOUNDING BOXES
                        # ---------------------------------

                        st.session_state.bounding_boxes = (
                            answer_data.get(
                                "bounding_boxes",
                                []
                            )
                        )


                        # ---------------------------------
                        # SAVE AI ANSWER
                        # ---------------------------------

                        st.session_state.chat_history.append(
                            {
                                "role": "assistant",
                                "content": answer
                            }
                        )


                        st.rerun()


                    else:

                        st.session_state.chat_history.append(
                            {
                                "role": "assistant",
                                "content": (
                                    f"Backend Error: "
                                    f"{response.text}"
                                )
                            }
                        )

                        st.rerun()


                except Exception as e:

                    st.session_state.chat_history.append(
                        {
                            "role": "assistant",
                            "content": (
                                f"Could not connect to backend: {e}"
                            )
                        }
                    )

                    st.rerun()


            else:

                st.warning(
                    "Please enter a question."
                )