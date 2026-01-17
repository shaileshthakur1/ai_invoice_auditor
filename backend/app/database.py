from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Boolean, DateTime, Text, Integer, ForeignKey
from datetime import datetime
from sqlalchemy.orm import Session

DATABASE_URL = "sqlite:///./invoice_auditor.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(String, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    ocr_used = Column(Boolean, default=False)
    raw_text = Column(Text, nullable=False)

    # 🔹 HITL fields
    status = Column(String, default="PROCESSED")  
    review_notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)


class InvoiceField(Base):
    __tablename__ = "invoice_fields"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(String, ForeignKey("invoices.id"))
    field = Column(String, index=True)
    value = Column(String)


class QueryLog(Base):
    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(String, ForeignKey("invoices.id"))
    question = Column(Text)
    answer = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()