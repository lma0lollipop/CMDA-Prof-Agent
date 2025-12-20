"""
pdf_utils.py

Utilities for extracting and preparing PDF content
as authoritative reference material for CMDAProfAgent.
"""

import pdfplumber


def extract_text_from_pdf(uploaded_pdf) -> str:
    """
    Extract raw text from a PDF file using pdfplumber.

    Parameters:
    uploaded_pdf : UploadedFile (Streamlit)

    Returns:
    str : Extracted text content
    """

    extracted_text = []

    try:
        with pdfplumber.open(uploaded_pdf) as pdf:
            for page_number, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text()
                if page_text:
                    extracted_text.append(
                        f"\n--- PAGE {page_number} ---\n{page_text}"
                    )

    except Exception as e:
        return f"PDF EXTRACTION ERROR: {e}"

    return "\n".join(extracted_text).strip()


def build_pdf_context(pdf_text: str) -> str:
    """
    Wrap extracted PDF text in a strict context block
    so the agent treats it as authoritative course material.
    """

    if not pdf_text:
        return ""

    return f"""
================ PDF CONTENT START ================
The following content has been extracted directly
from a PDF provided by the student.

This PDF represents AUTHORITATIVE course material.
All explanations, formulas, notation, and solution
methods MUST strictly follow this content.

If a required formula or method is NOT present in
the PDF, explicitly state that it is not available
in the provided material.

PDF TEXT:
{pdf_text}
================ PDF CONTENT END ==================
"""
