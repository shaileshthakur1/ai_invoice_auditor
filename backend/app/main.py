from fastapi import FastAPI
from app.database import Base, engine
from app.api.upload import router as upload_router
from app.api.chat import router as chat_router
from app.api.review import router as review_router
from app.api.invoice import router as invoice_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Invoice Auditor")

app.include_router(invoice_router, prefix="/invoice")
app.include_router(review_router, prefix="/review")
app.include_router(upload_router, prefix="/upload")
app.include_router(chat_router, prefix="/chat")

@app.get("/")
def health_check():
    return {"status": "Invoice Auditor running"}
