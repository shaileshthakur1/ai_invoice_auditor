import pytesseract
from PIL import Image


def run_ocr_on_image(image: Image.Image) -> str:
    """
    Run OCR on an image and return extracted text.
    """

    try:
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        raise RuntimeError(f"OCR failed: {e}")
