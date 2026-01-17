from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import (
    get_db,
    Invoice,
    InvoiceField,
    QueryLog
)
from app.rag.vector_store import load_vector_store
from app.rag.qa_chain import answer_question
from app.rag.router import (
    match_structured_field,
    answer_from_structured_db
)

router = APIRouter()


# =========================
# Request Schemas
# =========================
class ChatRequest(BaseModel):
    invoice_id: str
    question: str


# =========================
# Chat Endpoint
# =========================
@router.post("/")
def chat_with_invoice(
    payload: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Intelligent chat endpoint:
    - HITL aware
    - Structured DB → RAG fallback
    - Logs every query
    """

    # 🔹 HITL check
    invoice = (
        db.query(Invoice)
        .filter(Invoice.id == payload.invoice_id)
        .first()
    )

    if not invoice:
        return {
            "answer": "Invoice not found",
            "source": "error"
        }

    if invoice.status == "NEEDS_REVIEW":
        return {
            "answer": (
                "⚠️ This invoice is flagged for human review. "
                "Answers may be unreliable until approved."
            ),
            "source": "human_review"
        }

    answer = None
    source = "rag"

    # 1️⃣ Structured DB first
    matched_field = match_structured_field(payload.question)

    if matched_field:
        structured_answer = answer_from_structured_db(
            db=db,
            invoice_id=payload.invoice_id,
            field=matched_field
        )
        if structured_answer:
            answer = structured_answer
            source = "structured_db"

    # 2️⃣ RAG fallback
    if not answer:
        vector_store = load_vector_store(payload.invoice_id)
        documents = vector_store.similarity_search(
            payload.question,
            k=4
        )
        answer = answer_question(documents, payload.question)

    # 3️⃣ Log query
    log = QueryLog(
        invoice_id=payload.invoice_id,
        question=payload.question,
        answer=answer
    )
    db.add(log)
    db.commit()

    return {
        "answer": answer,
        "source": source
    }


# =========================
# Fetch Structured Fields
# =========================
@router.get("/fields/{invoice_id}")
def get_invoice_fields(
    invoice_id: str,
    db: Session = Depends(get_db)
):
    fields = (
        db.query(InvoiceField)
        .filter(InvoiceField.invoice_id == invoice_id)
        .all()
    )

    return {
        f.field: f.value
        for f in fields
    }


# =========================
# Fetch Query History
# =========================
@router.get("/history/{invoice_id}")
def get_query_history(
    invoice_id: str,
    db: Session = Depends(get_db)
):
    logs = (
        db.query(QueryLog)
        .filter(QueryLog.invoice_id == invoice_id)
        .order_by(QueryLog.created_at.desc())
        .all()
    )

    return [
        {
            "question": log.question,
            "answer": log.answer,
            "created_at": log.created_at
        }
        for log in logs
    ]
