import re
from sqlalchemy.orm import Session
from typing import Optional

from app.database import InvoiceField


STRUCTURED_FIELD_MAP = {
    "invoice_number": [
        r"invoice\s*number",
        r"invoice\s*no"
    ],
    "invoice_date": [
        r"invoice\s*date",
        r"date"
    ],
    "total_amount": [
        r"total\s*amount",
        r"grand\s*total",
        r"total"
    ],
    "vendor": [
        r"vendor",
        r"supplier",
        r"company"
    ]
}


def match_structured_field(question: str) -> Optional[str]:
    """
    Match user question to a structured field.
    """
    question = question.lower()

    for field, patterns in STRUCTURED_FIELD_MAP.items():
        for pattern in patterns:
            if re.search(pattern, question):
                return field

    return None


def answer_from_structured_db(
    db: Session,
    invoice_id: str,
    field: str
) -> Optional[str]:
    """
    Fetch structured field value from DB.
    """

    record = (
        db.query(InvoiceField)
        .filter(
            InvoiceField.invoice_id == invoice_id,
            InvoiceField.field == field
        )
        .first()
    )

    if record:
        return record.value

    return None
