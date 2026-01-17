# 🧾 Invoice Auditor

An **AI-powered invoice auditing system** that extracts structured data from invoices, enables intelligent question answering using RAG, and supports **Human-in-the-Loop (HITL)** review for approval, rejection, and correction of invoice data.

---

## 📌 Project Overview

**Invoice Auditor** is an end-to-end application designed for real-world invoice verification workflows.  
It combines deterministic data extraction, vector-based retrieval, and human oversight to ensure accuracy and audit safety.

The system is built with a **backend–frontend separation**, persistent storage, and invoice-level isolation.

---

## 🔄 Application Workflow

1. **Invoice Upload** – PDF or image invoices are uploaded  
2. **Text Extraction** – PDF parsing / OCR (if required)  
3. **Structured Extraction** – Key invoice fields extracted deterministically  
4. **Vector Indexing** – Invoice text embedded and stored per invoice  
5. **Human-in-the-Loop Review**
   - Approve
   - Reject
   - Edit extracted fields
6. **AI Question Answering**
   - Structured DB lookup first
   - RAG fallback when needed
7. **Query Logging & Audit Trail**

---

## 🏗️ Project Structure

```text 
invoice-auditor/
│
├── backend/
│ ├── app/
│ │ ├── api/ # FastAPI routes (upload, chat, review, invoice)
│ │ ├── ingestion/ # File loading, OCR, parsing, extraction
│ │ ├── rag/ # Embeddings, vector store, routing logic
│ │ ├── database.py # SQLAlchemy models & DB session
│ │ ├── config.py # Environment configuration
│ │ └── main.py # FastAPI entry point
│ │
│ └── .env.example
│
├── ui/
│ └── streamlit_app.py # Streamlit-based UI
│
├── data/
│ ├── uploads/ # Uploaded invoices (runtime)
│ └── vector_db/ # Per-invoice vector stores (runtime)
│
├── requirements.txt
├── .gitignore
└── README.md

```yaml 

---

## 🧠 Core Capabilities

### 🔍 Structured Invoice Extraction
- Invoice number
- Invoice date
- Vendor name
- Total amount  
(Deterministic, non-LLM based)

### 🧠 AI Question Answering (RAG)
- Invoice-specific retrieval
- No cross-invoice context leakage
- Answers always scoped to the selected invoice

### 🧑‍⚖️ Human-in-the-Loop (HITL)
- Approve invoice
- Reject invoice
- Edit extracted fields
- Edited data is persisted and immediately reflected in AI answers

### 📜 Auditability
- All queries and answers are logged
- Invoice state is tracked (processed / reviewed / approved)

---

## 🖥️ User Interface (Streamlit)

- Upload single or multiple invoices
- Select invoice context from sidebar
- Expandable sections for:
  - Extracted invoice information
  - Review & actions
- AI assistant for invoice-specific questions
- Scrollable query history per invoice

---

## ⚙️ LLM & Embedding Strategy

- **Default provider:** Cohere (chat + embeddings)
- **Optional fallbacks:** OpenAI, Gemini
- Each invoice has:
  - its own database records
  - its own vector index
- Ensures strict data isolation and audit safety

---

## ▶️ Running the Application

### 1️⃣ Start Backend (FastAPI)

```bash
cd backend
uvicorn app.main:app --reload

API available at:

```bash
http://127.0.0.1:8000

Swagger docs:
```bash
http://127.0.0.1:8000/docs

2️⃣ Start UI (Streamlit)
```bash
cd ui
streamlit run streamlit_app.py


🎯 Use Cases

Invoice verification & auditing

Finance and accounting workflows

Compliance-oriented document review

AI-assisted invoice analysis

📌 Future Enhancements

Rule-based auto-flagging

Role-based access control

Confidence scoring for extracted fields

Reporting & analytics dashboard

Containerized deployment

🏁 Summary

This project demonstrates a production-oriented invoice auditing pipeline that balances automation with human oversight.
It is designed to be accurate, auditable, and extensible, making it suitable for real-world financial document workflows.