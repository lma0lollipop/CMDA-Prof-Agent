"""
image_utils.py

Utilities for extracting and preparing text from images
(classroom notes, handwritten questions, scanned problems)
for CMDAProfAgent.
"""

from PIL import Image
import io
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"



def extract_text_from_image(uploaded_image) -> str:
    """
    Extract text from an uploaded image using pytesseract OCR.

    Parameters:
    uploaded_image : UploadedFile (Streamlit)

    Returns:
    str : Extracted text
    """

    try:
        # Convert uploaded file to PIL Image
        image_bytes = uploaded_image.read()
        image = Image.open(io.BytesIO(image_bytes))

        # Optional: convert to grayscale for better OCR
        image = image.convert("L")

        text = pytesseract.image_to_string(image)

        return text.strip()

    except Exception as e:
        return f"IMAGE OCR ERROR: {e}"


def build_image_context(image_text: str) -> str:
    """
    Wrap OCR-extracted image text in a strict context block
    so the agent treats it as authoritative classroom material.
    """

    if not image_text:
        return ""

    return f"""
================ IMAGE CONTENT START ================
The following content has been extracted from an image
uploaded by the student.

This image represents CLASSROOM NOTES or a QUESTION
written or provided by the instructor.

Treat this content as AUTHORITATIVE.
Use the SAME formulas, notation, symbols, and solution
steps exactly as they appear here.

Do NOT introduce alternative formulas or methods.
If the image does not contain a required formula,
explicitly state that it is not available in the image.

IMAGE TEXT:
{image_text}
================ IMAGE CONTENT END ==================
"""
