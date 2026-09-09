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

st.set_page_config(
    page_title="AI Document Extractor",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# SESSION STATE
# =========================================================

DEFAULT_STATE = {
    "result": None,
    "uploaded_file_data": None,
    "uploaded_file_name": None,
    "uploaded_file_type": None,
    "chat_history": [],
    "bounding_boxes": [],
}

for key, value in DEFAULT_STATE.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# DARK THEME CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       MAIN APP
    ===================================================== */

    .stApp {
        background-color: #0f1117;
        color: #f8fafc;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }


    /* =====================================================
       HEADER
    ===================================================== */

    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #f8fafc;
        margin-bottom: 5px;
    }

    .main-subtitle {
        font-size: 17px;
        color: #94a3b8;
        margin-bottom: 30px;
    }


    /* =====================================================
       UPLOAD
    ===================================================== */

    .upload-title {
        font-size: 22px;
        font-weight: 700;
        color: #f8fafc;
    }

    .upload-subtitle {
        font-size: 15px;
        color: #94a3b8;
        margin-bottom: 12px;
    }


    /* =====================================================
       STREAMLIT TEXT
    ===================================================== */

    p,
    label,
    .stMarkdown,
    .stCaption {
        color: #e2e8f0;
    }


    /* =====================================================
       FILE UPLOADER
    ===================================================== */

    [data-testid="stFileUploader"] {
        background-color: #1a1d25;
        border: 1px solid #2d3340;
        border-radius: 12px;
    }

    [data-testid="stFileUploaderDropzone"] {
        background-color: #1a1d25;
        border: 1px dashed #3f4654;
    }


    /* =====================================================
       BUTTONS
    ===================================================== */

    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }


    /* =====================================================
       CONTAINERS
    ===================================================== */

    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #171a21;
        border: 1px solid #2d3340;
        border-radius: 16px;
    }


    /* =====================================================
       HEADINGS
    ===================================================== */

    h1,
    h2,
    h3,
    h4 {
        color: #f8fafc !important;
    }


    /* =====================================================
       INFO / SUCCESS
    ===================================================== */

    [data-testid="stAlert"] {
        border-radius: 10px;
    }


    /* =====================================================
       TEXT AREA
    ===================================================== */

    textarea {
        background-color: #111318 !important;
        color: #e2e8f0 !important;
        border: 1px solid #303642 !important;
    }


    /* =====================================================
       JSON
    ===================================================== */

    [data-testid="stJson"] {
        background-color: #111318;
        border-radius: 10px;
    }


    /* =====================================================
       DIVIDER
    ===================================================== */

    hr {
        border-color: #2d3340;
    }


    /* =====================================================
       FLOATING CHAT BUTTON
    ===================================================== */

    div[data-testid="stPopover"] {
        position: fixed !important;

        right: 24px !important;
        bottom: 24px !important;

        left: auto !important;
        top: auto !important;

        width: 58px !important;
        min-width: 58px !important;
        max-width: 58px !important;

        height: 58px !important;
        min-height: 58px !important;

        z-index: 999999 !important;

        margin: 0 !important;
        padding: 0 !important;
    }


    div[data-testid="stPopover"] > button {
        width: 58px !important;
        height: 58px !important;

        border-radius: 50% !important;

        padding: 0 !important;

        font-size: 24px !important;
    }


    /* =====================================================
       CHAT POPUP
    ===================================================== */

    div[data-testid="stPopoverBody"] {
        background-color: #171a21 !important;
        border: 1px solid #303642 !important;
    }


    /* =====================================================
       CHAT INPUT
    ===================================================== */

    div[data-baseweb="input"] {
        background-color: #111318 !important;
    }

    div[data-baseweb="input"] input {
        color: #f8fafc !important;
    }


    /* =====================================================
       IMAGE
    ===================================================== */

    img {
        border-radius: 10px;
    }


    /* =====================================================
       FOOTER
    ===================================================== */

    .footer-text {
        text-align: center;
        color: #64748b;
        font-size: 13px;
        padding-top: 25px;
        padding-bottom: 15px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">📄 AI Document Extractor</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="main-subtitle">'
    'Upload a document and let AI extract structured information automatically.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# UPLOAD SECTION
# =========================================================

st.markdown(
    '<div class="upload-title">Upload Document</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="upload-subtitle">'
    'Supported documents can be analyzed using OCR and AI.'
    '</div>',
    unsafe_allow_html=True
)


uploaded_file = st.file_uploader(
    "Choose a document",
    type=[
        "png",
        "jpg",
        "jpeg",
        "webp",
        "pdf"
    ],
    label_visibility="collapsed"
)


# =========================================================
# HANDLE FILE
# =========================================================

if uploaded_file is not None:

    new_file_data = uploaded_file.getvalue()
    new_file_name = uploaded_file.name
    new_file_type = uploaded_file.type

    if (
        st.session_state.uploaded_file_name != new_file_name
        or st.session_state.uploaded_file_data != new_file_data
    ):

        st.session_state.result = None
        st.session_state.chat_history = []
        st.session_state.bounding_boxes = []

        st.session_state.uploaded_file_data = new_file_data
        st.session_state.uploaded_file_name = new_file_name
        st.session_state.uploaded_file_type = new_file_type


# =========================================================
# ANALYZE BUTTON
# =========================================================

if uploaded_file is not None:

    if st.button(
        "🔍 Analyze Document",
        type="primary",
        use_container_width=True
    ):

        with st.spinner(
            "AI is analyzing your document..."
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
                    timeout=180
                )

                if response.status_code == 200:

                    st.session_state.result = response.json()

                    st.session_state.chat_history = []

                    st.session_state.bounding_boxes = []

                    st.success(
                        "Document analyzed successfully! ✅"
                    )

                    st.rerun()

                else:

                    st.error(
                        f"Backend error: {response.text}"
                    )

            except requests.exceptions.ConnectionError:

                st.error(
                    "❌ Could not connect to backend. "
                    "Make sure FastAPI is running."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "❌ Request timed out."
                )

            except Exception as e:

                st.error(
                    f"❌ Error: {str(e)}"
                )


# =========================================================
# RESULT
# =========================================================

result = st.session_state.result


if result is not None:

    # =====================================================
    # PROCESSING PIPELINE
    # =====================================================

    with st.container(border=True):

        st.subheader(
            "⚙️ AI Processing Pipeline"
        )

        pipeline_columns = st.columns(9)

        with pipeline_columns[0]:
            st.info("📤 Upload")

        with pipeline_columns[1]:
            st.markdown("### →")

        with pipeline_columns[2]:
            st.info("🔎 OCR")

        with pipeline_columns[3]:
            st.markdown("### →")

        with pipeline_columns[4]:
            st.info("🧠 Detection")

        with pipeline_columns[5]:
            st.markdown("### →")

        with pipeline_columns[6]:
            st.info("🤖 Extraction")

        with pipeline_columns[7]:
            st.markdown("### →")

        with pipeline_columns[8]:
            st.info("📦 JSON")


    st.write("")


    # =====================================================
    # MAIN COLUMNS
    # =====================================================

    left_column, right_column = st.columns(
        [1.05, 1],
        gap="large"
    )


    # =====================================================
    # LEFT COLUMN
    # =====================================================

    with left_column:

        with st.container(border=True):

            st.subheader(
                "📑 Document Preview"
            )

            file_data = (
                st.session_state.uploaded_file_data
            )

            file_type = (
                st.session_state.uploaded_file_type
                or ""
            )


            # =============================================
            # IMAGE PREVIEW
            # =============================================

            if (
                file_data
                and file_type.startswith("image/")
            ):

                try:

                    image = Image.open(
                        BytesIO(file_data)
                    ).convert("RGB")


                    draw = ImageDraw.Draw(
                        image
                    )


                    bounding_boxes = (
                        st.session_state.get(
                            "bounding_boxes",
                            []
                        )
                    )


                    box_count = 0


                    for item in bounding_boxes:

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

                            # ---------------------------------
                            # RECTANGLE
                            # ---------------------------------

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


                                draw.rectangle(
                                    [
                                        x1,
                                        y1,
                                        x2,
                                        y2
                                    ],
                                    outline="#ff3030",
                                    width=5
                                )


                                box_count += 1


                            # ---------------------------------
                            # POLYGON
                            # ---------------------------------

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

                                    points.append(
                                        points[0]
                                    )


                                    draw.line(
                                        points,
                                        fill="#ff3030",
                                        width=5
                                    )


                                    box_count += 1


                        except Exception:

                            continue


                    # -------------------------------------
                    # DISPLAY IMAGE
                    # -------------------------------------

                    st.image(
                        image,
                        use_container_width=True
                    )


                    if box_count > 0:

                        st.success(
                            f"🔴 {box_count} "
                            f"matching field(s) highlighted"
                        )


                except Exception as e:

                    st.error(
                        f"Could not display image: {e}"
                    )


            # =============================================
            # PDF
            # =============================================

            elif (
                file_data
                and file_type == "application/pdf"
            ):

                encoded_pdf = base64.b64encode(
                    file_data
                ).decode("utf-8")


                pdf_display = f"""
                <iframe
                    src="data:application/pdf;base64,{encoded_pdf}"
                    width="100%"
                    height="650"
                    style="
                        border:1px solid #303642;
                        border-radius:12px;
                        background:#171a21;
                    ">
                </iframe>
                """


                st.markdown(
                    pdf_display,
                    unsafe_allow_html=True
                )


            else:

                st.info(
                    "Document preview is not available."
                )


    # =====================================================
    # RIGHT COLUMN
    # =====================================================

    with right_column:

        with st.container(border=True):

            st.subheader(
                "🧠 Extracted Information"
            )


            document_type = result.get(
                "document_type",
                "Unknown"
            )


            st.info(
                f"📄 Document Type: {document_type}"
            )


            structured_data = result.get(
                "data",
                {}
            )


            if isinstance(
                structured_data,
                dict
            ):

                for key, value in structured_data.items():

                    if value is None:
                        value = "Not found"


                    label = (
                        str(key)
                        .replace(
                            "_",
                            " "
                        )
                        .title()
                    )


                    field_col1, field_col2 = st.columns(
                        [1, 1.5]
                    )


                    with field_col1:

                        st.caption(
                            label
                        )


                    with field_col2:

                        st.write(
                            str(value)
                        )


                    st.divider()


            else:

                st.write(
                    structured_data
                )


    # =====================================================
    # RAW OCR
    # =====================================================

    st.write("")


    with st.container(border=True):

        st.subheader(
            "🔎 Raw OCR Text"
        )


        extracted_text = result.get(
            "extracted_text",
            []
        )


        if isinstance(
            extracted_text,
            list
        ):

            raw_text = "\n".join(
                str(text)
                for text in extracted_text
            )

        else:

            raw_text = str(
                extracted_text
            )


        st.text_area(
            "OCR Text",
            raw_text,
            height=220,
            label_visibility="collapsed"
        )


    # =====================================================
    # STRUCTURED JSON
    # =====================================================

    st.write("")


    with st.container(border=True):

        st.subheader(
            "📦 Structured JSON"
        )


        st.json(
            structured_data
        )


        json_data = json.dumps(
            structured_data,
            indent=4,
            ensure_ascii=False
        )


        st.download_button(
            label="⬇️ Download JSON",
            data=json_data,
            file_name="extracted_data.json",
            mime="application/json",
            use_container_width=True
        )


    # =====================================================
    # NEW DOCUMENT
    # =====================================================

    st.write("")


    if st.button(
        "🔄 Analyze New Document",
        use_container_width=True
    ):

        st.session_state.result = None

        st.session_state.uploaded_file_data = None

        st.session_state.uploaded_file_name = None

        st.session_state.uploaded_file_type = None

        st.session_state.chat_history = []

        st.session_state.bounding_boxes = []

        st.rerun()


# =========================================================
# FLOATING CHAT
# =========================================================

if result is not None:

    with st.popover("💬"):

        st.subheader(
            "💬 Ask Your Document"
        )

        st.caption(
            "Ask questions about the uploaded document."
        )


        # =================================================
        # CHAT HISTORY
        # =================================================

        for message in st.session_state.chat_history:

            role = message.get(
                "role"
            )

            content = message.get(
                "content",
                ""
            )


            if role == "user":

                st.chat_message(
                    "user"
                ).write(
                    content
                )

            else:

                st.chat_message(
                    "assistant"
                ).write(
                    content
                )


        # =================================================
        # QUESTION INPUT
        # =================================================

        question = st.text_input(
            "Ask a question",
            placeholder="e.g. What is the date of birth?",
            key="document_question_input"
        )


        ask_button = st.button(
            "Ask",
            use_container_width=True
        )


        # =================================================
        # ASK QUESTION
        # =================================================

        if ask_button:

            if not question.strip():

                st.warning(
                    "Please enter a question."
                )

            else:

                with st.spinner(
                    "AI is thinking..."
                ):

                    try:

                        response = requests.post(
                            f"{BACKEND_URL}/ask",
                            params={
                                "question": question
                            },
                            timeout=120
                        )


                        if response.status_code == 200:

                            answer_data = (
                                response.json()
                            )


                            answer = (
                                answer_data.get(
                                    "answer",
                                    "No answer received."
                                )
                            )


                            # ---------------------------------
                            # BOUNDING BOXES
                            # ---------------------------------

                            st.session_state.bounding_boxes = (
                                answer_data.get(
                                    "bounding_boxes",
                                    []
                                )
                            )


                            # ---------------------------------
                            # CHAT HISTORY
                            # ---------------------------------

                            st.session_state.chat_history.append(
                                {
                                    "role": "user",
                                    "content": question
                                }
                            )


                            st.session_state.chat_history.append(
                                {
                                    "role": "assistant",
                                    "content": answer
                                }
                            )


                            st.rerun()


                        else:

                            st.error(
                                f"Backend error: {response.text}"
                            )


                    except requests.exceptions.ConnectionError:

                        st.error(
                            "❌ Could not connect to backend."
                        )


                    except requests.exceptions.Timeout:

                        st.error(
                            "❌ AI request timed out."
                        )


                    except Exception as e:

                        st.error(
                            f"❌ Error: {str(e)}"
                        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer-text">'
    'AI Document Extractor • OCR + AI + Document Q&A'
    '</div>',
    unsafe_allow_html=True
)