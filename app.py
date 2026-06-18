import os
import tempfile

import streamlit as st
from markitdown import MarkItDown


# -------------------------
# Page Configuration
# -------------------------

st.set_page_config(
    page_title="Document to Markdown Converter",
    page_icon="📝",
    layout="wide"
)

st.title("📝 Document to Markdown Converter")

st.markdown(
    """
Upload a supported document and convert it into **Markdown (.md)**.

Powered by **Microsoft MarkItDown**.
"""
)


# -------------------------
# File Upload
# -------------------------

uploaded_file = st.file_uploader(
    "Choose a document"
)


# -------------------------
# Conversion
# -------------------------

if uploaded_file is not None:

    file_extension = os.path.splitext(uploaded_file.name)[1]

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=file_extension
    ) as temp_file:

        temp_file.write(uploaded_file.getbuffer())
        temp_path = temp_file.name

    try:

        converter = MarkItDown()

        result = converter.convert(temp_path)

        markdown_text = result.text_content

        st.success("✅ Conversion completed successfully!")

        st.subheader("Markdown Preview")

        st.text_area(
            label="",
            value=markdown_text,
            height=500
        )

        st.download_button(
            label="⬇️ Download Markdown",
            data=markdown_text,
            file_name=f"{os.path.splitext(uploaded_file.name)[0]}.md",
            mime="text/markdown"
        )

    except Exception as e:

        st.error("❌ Conversion failed.")

        st.exception(e)

    finally:

        if os.path.exists(temp_path):
            os.remove(temp_path)