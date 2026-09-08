import json
import base64
import requests
import html
import streamlit as st


# =========================================================
# CONFIGURATION
# =========================================================

API_URL = "http://127.0.0.1:8000/upload"

st.set_page_config(
    page_title="AI Document Extractor",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
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


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

.stApp {
    background: #0b0d10;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* ================= HEADER ================= */

.brand-row {
    display: flex;
    align-items: center;
    gap: 14px;
}

.brand-icon {
    width: 46px;
    height: 46px;
    border-radius: 12px;
    background: #f4f5f7;
    color: #0b0d10;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 23px;
    font-weight: 800;
}

.brand-title {
    color: #f5f7fa;
    font-size: 30px;
    font-weight: 750;
    letter-spacing: -0.8px;
}

.subtitle {
    color: #858b95;
    font-size: 14px;
    margin-top: 7px;
    margin-left: 60px;
}

.online {
    text-align: right;
    color: #aab0b8;
    font-size: 13px;
    margin-top: 12px;
}

.online-dot {
    color: #4fd184;
    font-size: 15px;
}

.top-divider {
    height: 1px;
    background: #22262d;
    margin: 27px 0 30px 0;
}

/* ================= UPLOAD ================= */

.upload-heading {
    color: #f1f3f5;
    font-size: 19px;
    font-weight: 650;
}

.upload-description {
    color: #777e88;
    font-size: 13px;
    margin-top: 5px;
    margin-bottom: 16px;
}

/* ================= PANELS ================= */

.panel {
    background: #111419;
    border: 1px solid #252a32;
    border-radius: 16px;
    padding: 20px;
}

.panel-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 18px;
}

.panel-title {
    color: #f2f4f6;
    font-size: 17px;
    font-weight: 650;
}

.panel-label {
    color: #68707a;
    font-size: 10px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ================= DOCUMENT TYPE ================= */

.document-type {
    background: #171b21;
    border: 1px solid #2a3038;
    border-radius: 12px;
    padding: 15px 17px;
    margin-bottom: 15px;
}

.document-type-value {
    color: #f4f6f8;
    font-size: 19px;
    font-weight: 650;
    margin-top: 5px;
}

/* ================= FIELD CARD ================= */

.field-card {
    background: #171b21;
    border: 1px solid #252b33;
    border-radius: 11px;
    padding: 13px 15px;
    margin-bottom: 10px;
    min-height: 72px;
}

.field-label {
    color: #707782;
    font-size: 10px;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    margin-bottom: 6px;
}

.field-value {
    color: #e8ebef;
    font-size: 14px;
    font-weight: 550;
    word-break: break-word;
}

/* ================= PIPELINE ================= */

.pipeline {
    display: flex;
    align-items: center;
    justify-content: center;
    background: #111419;
    border: 1px solid #252a32;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 22px;
}

.pipeline-step {
    display: flex;
    align-items: center;
    gap: 9px;
}

.pipeline-icon {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #14261c;
    border: 1px solid #2b6945;
    color: #67d996;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    font-weight: 700;
}

.pipeline-text {
    color: #dce1e6;
    font-size: 12px;
    font-weight: 550;
}

.pipeline-line {
    width: 55px;
    height: 1px;
    background: #303640;
    margin: 0 14px;
}

@media (max-width: 900px) {

    .pipeline {
        flex-direction: column;
        align-items: flex-start;
        gap: 12px;
    }

    .pipeline-line {
        width: 1px;
        height: 20px;
        margin: 0 0 0 13px;
    }

}

/* ================= SUCCESS ================= */

.success-box {
    background: #0f1914;
    border: 1px solid #244a35;
    color: #70d99b;
    padding: 11px 15px;
    border-radius: 10px;
    font-size: 13px;
    margin-bottom: 20px;
}

/* ================= FILE INFO ================= */

.file-info {
    color: #777f89;
    font-size: 12px;
    margin-top: 8px;
}

.file-name {
    color: #d8dde3;
    font-weight: 600;
}

/* ================= FOOTER ================= */

.footer {
    text-align: center;
    color: #505761;
    font-size: 11px;
    margin-top: 35px;
}

</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# HEADER
# =========================================================

header_left, header_right = st.columns([4, 1])

with header_left:

    st.markdown(
        """
<div class="brand-row">
    <div class="brand-icon">◈</div>
    <div class="brand-title">AI Document Extractor</div>
</div>

<div class="subtitle">
    Intelligent document processing & structured information extraction
</div>
""",
        unsafe_allow_html=True,
    )


with header_right:

    st.markdown(
        """
<div class="online">
    <span class="online-dot">●</span>
    System Online
</div>
""",
        unsafe_allow_html=True,
    )


st.markdown(
    '<div class="top-divider"></div>',
    unsafe_allow_html=True,
)


# =========================================================
# UPLOAD SECTION
# =========================================================

st.markdown(
    '<div class="upload-heading">Upload Document</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="upload-description">
    Upload a document image or PDF. The system will automatically
    detect the document type and extract relevant information.
</div>
""",
    unsafe_allow_html=True,
)


uploaded_file = st.file_uploader(
    "Choose document",
    type=["jpg", "jpeg", "png", "pdf"],
    label_visibility="collapsed",
)


# =========================================================
# NEW FILE SELECTED
# =========================================================

if uploaded_file is not None:

    # Detect if user selected a different file
    current_name = uploaded_file.name

    if (
        st.session_state.uploaded_file_name != current_name
    ):

        st.session_state.result = None

        st.session_state.uploaded_file_data = (
            uploaded_file.getvalue()
        )

        st.session_state.uploaded_file_name = (
            uploaded_file.name
        )

        st.session_state.uploaded_file_type = (
            uploaded_file.type
        )


    file_size_kb = uploaded_file.size / 1024

    st.markdown(
        f"""
<div class="file-info">
    Selected:
    <span class="file-name">{html.escape(uploaded_file.name)}</span>
    &nbsp; • &nbsp;
    {file_size_kb:.1f} KB
</div>
""",
        unsafe_allow_html=True,
    )


    st.write("")


    # =====================================================
    # ANALYZE BUTTON
    # =====================================================

    if st.button(
        "Analyze Document",
        type="primary",
        use_container_width=True,
    ):

        with st.spinner(
            "Analyzing document with AI..."
        ):

            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type,
                )
            }

            try:

                response = requests.post(
                    API_URL,
                    files=files,
                    timeout=180,
                )


                if response.status_code == 200:

                    st.session_state.result = (
                        response.json()
                    )

                    st.rerun()


                else:

                    st.error(
                        f"Backend Error: {response.status_code}"
                    )

                    try:

                        st.json(
                            response.json()
                        )

                    except Exception:

                        st.write(
                            response.text
                        )


            except requests.exceptions.Timeout:

                st.error(
                    "The document took too long to process. "
                    "Please try again."
                )


            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to FastAPI backend. "
                    "Make sure the backend server is running."
                )


            except Exception as e:

                st.error(
                    f"Something went wrong: {str(e)}"
                )


# =========================================================
# RESULT SECTION
# =========================================================

if st.session_state.result is not None:

    result = st.session_state.result

    file_data = st.session_state.uploaded_file_data
    file_name = st.session_state.uploaded_file_name
    file_type = st.session_state.uploaded_file_type


    # =====================================================
    # SUCCESS
    # =====================================================

    st.markdown(
        """
        <div class="success-box">
            ✓ Document processed successfully
        </div>
        """,
        unsafe_allow_html=True,
    )

    # =====================================================
    # AI PROCESSING PIPELINE
    # =====================================================

    st.markdown(
        '<div class="pipeline">'
        '<div class="pipeline-step">'
        '<div class="pipeline-icon">✓</div>'
        '<div class="pipeline-text">OCR</div>'
        '</div>'
        '<div class="pipeline-line"></div>'
        '<div class="pipeline-step">'
        '<div class="pipeline-icon">✓</div>'
        '<div class="pipeline-text">Document Detection</div>'
        '</div>'
        '<div class="pipeline-line"></div>'
        '<div class="pipeline-step">'
        '<div class="pipeline-icon">✓</div>'
        '<div class="pipeline-text">AI Extraction</div>'
        '</div>'
        '<div class="pipeline-line"></div>'
        '<div class="pipeline-step">'
        '<div class="pipeline-icon">✓</div>'
        '<div class="pipeline-text">Structured Result</div>'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # MAIN COLUMNS
    # =====================================================

    left, right = st.columns(
        [1, 1],
        gap="large",
    )


    # =====================================================
    # LEFT — DOCUMENT PREVIEW
    # =====================================================

    with left:

        st.markdown(
            """
<div class="panel">

<div class="panel-header">

<div class="panel-title">
📄 Document Preview
</div>

<div class="panel-label">
SOURCE
</div>

</div>
""",
            unsafe_allow_html=True,
        )


        if file_data and file_type:

            # IMAGE PREVIEW

            if file_type.startswith("image/"):

                st.image(
                    file_data,
                    use_container_width=True,
                )


            # PDF PREVIEW

            elif file_type == "application/pdf":

                base64_pdf = base64.b64encode(
                    file_data
                ).decode("utf-8")

                pdf_html = f"""
<iframe
    src="data:application/pdf;base64,{base64_pdf}"
    width="100%"
    height="650"
    style="
        border: 1px solid #252a32;
        border-radius: 10px;
    "
>
</iframe>
"""

                st.markdown(
                    pdf_html,
                    unsafe_allow_html=True,
                )


        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


    # =====================================================
    # RIGHT — EXTRACTED INFORMATION
    # =====================================================

    with right:

        st.markdown(
            """
<div class="panel">

<div class="panel-header">

<div class="panel-title">
📋 Extracted Information
</div>

<div class="panel-label">
AI RESULT
</div>

</div>
""",
            unsafe_allow_html=True,
        )


        # =================================================
        # DOCUMENT TYPE
        # =================================================

        document_type = result.get(
            "document_type",
            "Unknown",
        )

        safe_document_type = html.escape(
            str(document_type)
        )

        st.markdown(
            f"""
            <div class="document-type">

            <div class="panel-label">
            Document Type
            </div>

            <div class="document-type-value">
            {safe_document_type}
            </div>

            </div>
            """,
            unsafe_allow_html=True,
        )


        # =================================================
        # EXTRACTED DATA
        # =================================================

        data = result.get(
            "data",
            {},
        )


        if isinstance(data, dict) and data:

            field_col_1, field_col_2 = st.columns(2)

            items = list(data.items())


            for index, (key, value) in enumerate(items):

                label = (
                    str(key)
                    .replace("_", " ")
                    .title()
                )

                safe_label = html.escape(
                    label
                )


                # VALUE FORMATTING

                if value is None:

                    display_value = "Not available"

                elif isinstance(value, bool):

                    display_value = (
                        "Yes"
                        if value
                        else "No"
                    )

                elif isinstance(value, (dict, list)):

                    display_value = json.dumps(
                        value,
                        ensure_ascii=False
                    )

                else:

                    display_value = str(value)


                safe_value = html.escape(
                    display_value
                )


                target_column = (
                    field_col_1
                    if index % 2 == 0
                    else field_col_2
                )


                with target_column:

                    st.markdown(
                        f"""
<div class="field-card">

<div class="field-label">
{safe_label}
</div>

<div class="field-value">
{safe_value}
</div>

</div>
""",
                        unsafe_allow_html=True,
                    )


        else:

            st.warning(
                "No structured information was extracted."
            )


        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )


    # =====================================================
    # ACTIONS
    # =====================================================

    st.write("")

    st.divider()


    action_1, action_2, action_3 = st.columns(
        [2, 2, 1]
    )


    # =====================================================
    # RAW OCR
    # =====================================================

    with action_1:

        with st.expander(
            "View Raw OCR Text"
        ):

            ocr_text = result.get(
                "extracted_text",
                []
            )


            if ocr_text:

                for text in ocr_text:

                    st.write(
                        str(text)
                    )

            else:

                st.info(
                    "No OCR text available."
                )


    # =====================================================
    # DOWNLOAD JSON
    # =====================================================

    with action_2:

        json_data = json.dumps(
            result,
            indent=4,
            ensure_ascii=False,
        )

        st.download_button(
            "Download JSON",
            data=json_data,
            file_name="extracted_document.json",
            mime="application/json",
            use_container_width=True,
        )


    # =====================================================
    # NEW DOCUMENT
    # =====================================================

    with action_3:

        if st.button(
            "New Document",
            use_container_width=True,
        ):

            st.session_state.result = None
            st.session_state.uploaded_file_data = None
            st.session_state.uploaded_file_name = None
            st.session_state.uploaded_file_type = None

            st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
<div class="footer">
    AI Document Extractor • OCR + Intelligent Information Extraction
</div>
""",
    unsafe_allow_html=True,
)