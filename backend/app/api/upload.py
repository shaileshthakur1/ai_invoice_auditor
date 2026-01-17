import uuid
from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from app.ingestion.loader import save_upload, load_document
from app.ingestion.parser import normalize_text
from app.rag.retriever import chunk_and_store
from app.database import Invoice, get_db
from app.ingestion.structured_extractor import extract_structured_fields
from app.database import InvoiceField


router = APIRouter()


@router.post("/")
def upload_invoice(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload invoice, extract text, persist data, create vector store.
    """

    invoice_id = str(uuid.uuid4())

    # 1. Save file
    file_path = save_upload(file)

    # 2. Extract text
    text, used_ocr = load_document(file_path)
    text = normalize_text(text)

    # 3. Persist invoice in DB
    invoice = Invoice(
        id=invoice_id,
        filename=file.filename,
        ocr_used=used_ocr,
        raw_text=text
    )
    db.add(invoice)
    db.commit()

        # 4. Extract structured fields
    structured_fields = extract_structured_fields(text)

    for field, value in structured_fields.items():
        db.add(
            InvoiceField(
                invoice_id=invoice_id,
                field=field,
                value=value
            )
        )

    db.commit()

    # 5. Create vector store
    chunk_and_store(text, invoice_id)

    return {
        "invoice_id": invoice_id,
        "ocr_used": used_ocr,
        "message": "Invoice processed and stored successfully"
    }
