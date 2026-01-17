from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.database import get_db, Invoice, InvoiceField

router = APIRouter()


# =========================
# Schemas
# =========================
class ReviewNote(BaseModel):
    note: str


class EditField(BaseModel):
    field: str
    value: str


# =========================
# Flag Invoice
# =========================
@router.post("/{invoice_id}/flag")
def flag_invoice(
    invoice_id: str,
    payload: ReviewNote,
    db: Session = Depends(get_db)
):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()

    if not invoice:
        return {"error": "Invoice not found"}

    invoice.status = "NEEDS_REVIEW"
    invoice.review_notes = payload.note
    db.commit()

    return {"message": "Invoice flagged for review"}


# =========================
# Approve Invoice
# =========================
@router.post("/{invoice_id}/approve")
def approve_invoice(
    invoice_id: str,
    db: Session = Depends(get_db)
):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()

    if not invoice:
        return {"error": "Invoice not found"}

    invoice.status = "APPROVED"
    db.commit()

    return {"message": "Invoice approved"}


# =========================
# Edit Structured Field
# =========================
@router.post("/{invoice_id}/edit-field")
def edit_invoice_field(
    invoice_id: str,
    payload: EditField,
    db: Session = Depends(get_db)
):
    record = (
        db.query(InvoiceField)
        .filter(
            InvoiceField.invoice_id == invoice_id,
            InvoiceField.field == payload.field
        )
        .first()
    )

    if record:
        record.value = payload.value
    else:
        db.add(
            InvoiceField(
                invoice_id=invoice_id,
                field=payload.field,
                value=payload.value
            )
        )

    db.commit()
    return {"message": "Field updated"}
