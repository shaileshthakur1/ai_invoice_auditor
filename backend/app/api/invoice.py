from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db, Invoice

router = APIRouter()

@router.get("/list")
def list_invoices(db: Session = Depends(get_db)):
    invoices = db.query(Invoice).order_by(Invoice.created_at.desc()).all()
    return [{"id": i.id, "filename": i.filename} for i in invoices]
