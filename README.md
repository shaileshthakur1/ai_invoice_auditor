# 🧾 AI Invoice Auditor

An **AI-powered invoice auditing system** that extracts structured data from invoices, enables intelligent question answering using **Retrieval-Augmented Generation (RAG)**, and supports **Human-in-the-Loop (HITL)** review for approval, rejection, and correction of invoice data.

---

## 🚀 Quick Start (Step-by-Step)

### 1️⃣ Go to backend & create virtual environment

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux
```

---

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Create `.env` file

```bash
copy .env.example .env       # Windows
# cp .env.example .env       # macOS / Linux
```

Edit `backend/.env` and add your **Cohere API key**:

```env
COHERE_API_KEY=your_cohere_api_key

UPLOAD_PATH=../data/uploads
VECTOR_DB_PATH=../data/vector_db
```

> ⚠️ `.env` should NOT be committed to GitHub.

---

### 4️⃣ Start Backend (FastAPI)

```bash
uvicorn app.main:app --reload
```

Backend will run at:

```text
http://127.0.0.1:8000
```

Swagger API docs:(optional, you may try !)

```text
http://127.0.0.1:8000/docs
```

---

### 5️⃣ Start UI (Streamlit)

Open a new terminal:

```bash
cd ui
streamlit run streamlit_app.py
```

---

## 📌 Project Overview

**AI Invoice Auditor** is an end-to-end application designed for real-world invoice verification workflows.

It combines:

* deterministic invoice data extraction
* vector-based retrieval (RAG)
* explicit human oversight

The system follows a **backend–frontend separation**, uses persistent storage, and ensures **invoice-level isolation**.

---

## 🔄 Application Workflow

1. **Invoice Upload** – PDF or image invoices are uploaded
2. **Text Extraction** – PDF parsing / OCR (if required)
3. **Structured Extraction** – Key invoice fields extracted deterministically
4. **Vector Indexing** – Invoice text embedded and stored per invoice
5. **Human-in-the-Loop Review**

   * Approve
   * Reject
   * Edit extracted fields
6. **AI Question Answering**

   * Structured DB lookup first
   * RAG fallback when needed
7. **Query Logging & Audit Trail**

---

## 🏗️ Project Structure

```text
invoice-auditor/
│
├── backend/
│   ├── app/
│   │   ├── api/              # FastAPI routes (upload, chat, review, invoice)
│   │   ├── ingestion/        # File loading, OCR, parsing
│   │   ├── rag/              # Embeddings, vector store, routing logic
│   │   ├── database.py       # SQLAlchemy models & DB session
│   │   ├── config.py         # Environment configuration
│   │   └── main.py           # FastAPI entry point
│   │
│   ├── requirements.txt
│   └── .env.example
│
├── ui/
│   └── streamlit_app.py      # Streamlit-based UI
│
├── data/
│   ├── uploads/              # Uploaded invoices (runtime)
│   └── vector_db/            # Per-invoice vector stores (runtime)
│
├── .gitignore
└── README.md
```

---

## 🧠 Core Capabilities

### 🔍 Structured Invoice Extraction

* Invoice number
* Invoice date
* Vendor name
* Total amount

*(Deterministic, non-LLM based)*

---

### 🧠 AI Question Answering (RAG)

* Invoice-specific retrieval
* No cross-invoice context leakage
* Answers always scoped to the selected invoice

---

### 🧑‍⚖️ Human-in-the-Loop (HITL)

* Approve invoice
* Reject invoice
* Edit extracted fields
* Edited data is persisted and immediately reflected in AI answers

---

### 📜 Auditability

* All questions and answers are logged
* Invoice state is tracked (processed / reviewed / approved)

---

## 🖥️ User Interface (Streamlit)

* Upload single or multiple invoices
* Select invoice context from sidebar
* Expandable sections for:

  * Extracted invoice information
  * Review & actions
* AI assistant for invoice-specific questions
* Scrollable query history per invoice

---

## ⚙️ LLM & Embedding Strategy

* **Provider:** Cohere (chat + embeddings)
* Each invoice has:

  * its own database records
  * its own vector index
* Ensures strict data isolation and audit safety

---

## 🎯 Use Cases

* Invoice verification & auditing
* Finance and accounting workflows
* Compliance-oriented document review
* AI-assisted invoice analysis

---

## 📌 Future Enhancements

* Rule-based auto-flagging
* Role-based access control
* Confidence scoring for extracted fields
* Reporting & analytics dashboard
* Containerized deployment

---

## 🏁 Summary

This project demonstrates a **production-oriented invoice auditing pipeline** that balances automation with human oversight.

It is designed to be **accurate, auditable, and extensible**, making it suitable for real-world financial document workflows.

---


