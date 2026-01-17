import os
from typing import Tuple
from pypdf import PdfReader
from PIL import Image

from app.config import settings
from app.ingestion.ocr import run_ocr_on_image


def save_upload(file) -> str:
    """
    Save uploaded file to disk safely.
    """
    os.makedirs(settings.UPLOAD_PATH, exist_ok=True)

    file_path = os.path.join(settings.UPLOAD_PATH, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path


def load_document(file_path: str) -> Tuple[str, bool]:
    """
    Load document and return:
    - extracted text
    - whether OCR was used
    """

    if file_path.lower().endswith(".pdf"):
        return load_pdf(file_path)

    if file_path.lower().endswith((".png", ".jpg", ".jpeg")):
        text = run_ocr_on_image(Image.open(file_path))
        return text, True

    raise ValueError("Unsupported file type")
    

def load_pdf(file_path: str) -> Tuple[str, bool]:
    reader = PdfReader(file_path)

    text = ""
    for page in reader.pages:
        page_text = page.extract_text() or ""
        text += page_text + "\n"

    # Heuristic: scanned PDF if text is too small
    if len(text.strip()) < 100:
        ocr_text = ""
        for page in reader.pages:
            image = page.to_image()
            ocr_text += run_ocr_on_image(image)
        return ocr_text, True

    return text, False
