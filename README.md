# Invoice Auditor 🧾  
AI-powered invoice analysis with Human-in-the-Loop verification

Invoice Auditor is an end-to-end application that allows users to upload invoices (PDF or images), extract structured information, and ask intelligent questions using Retrieval-Augmented Generation (RAG).

The system is built with **audit safety**, **human review**, and **explainability** as first-class concerns — making it suitable for real-world financial document review, not just demos.

---

## ✨ Key Features

- 📤 Upload **single or multiple invoices**
- 🔍 Automatic extraction of key invoice fields (deterministic, non-LLM)
- 🧠 Context-aware AI Q&A using RAG
- 🧑‍⚖️ Human-in-the-Loop (HITL) workflow:
  - Approve invoice
  - Reject invoice
  - Edit extracted fields
- 🗂️ Persistent storage:
  - Relational DB for audit data
  - Vector DB per invoice for semantic search
- 📜 Query history per invoice
- 🔄 Multi-LLM fallback:
  - Default: Cohere
  - Optional: OpenAI, Gemini
- 🎨 Clean, audit-grade Streamlit UI
- 🔒 No cross-invoice data leakage

---

## 🧠 How It Works (High-Level Flow)

# Invoice Auditor 🧾  
AI-powered invoice analysis with Human-in-the-Loop verification

Invoice Auditor is an end-to-end application that allows users to upload invoices (PDF or images), extract structured information, and ask intelligent questions using Retrieval-Augmented Generation (RAG).

The system is built with **audit safety**, **human review**, and **explainability** as first-class concerns — making it suitable for real-world financial document review, not just demos.

---

## ✨ Key Features

- 📤 Upload **single or multiple invoices**
- 🔍 Automatic extraction of key invoice fields (deterministic, non-LLM)
- 🧠 Context-aware AI Q&A using RAG
- 🧑‍⚖️ Human-in-the-Loop (HITL) workflow:
  - Approve invoice
  - Reject invoice
  - Edit extracted fields
- 🗂️ Persistent storage:
  - Relational DB for audit data
  - Vector DB per invoice for semantic search
- 📜 Query history per invoice
- 🔄 Multi-LLM fallback:
  - Default: Cohere
  - Optional: OpenAI, Gemini
- 🎨 Clean, audit-grade Streamlit UI
- 🔒 No cross-invoice data leakage

---

## 🧠 How It Works (High-Level Flow)

Invoice Upload
↓
Text Extraction (PDF parsing / OCR)
↓
Structured Field Extraction (Regex + heuristics)
↓
Vector Embedding (per invoice)
↓
Human Review (Approve / Reject / Edit)
↓
AI Question Answering
├─ Structured DB (if possible)
└─ RAG fallback (invoice-specific)


### Smart Query Routing
1. If a question maps to a known structured field → answer directly from DB  
2. Otherwise → retrieve relevant chunks from that invoice’s vector store  
3. All queries and answers are logged for auditability

---

## 🏗️ Project Structure

invoice-auditor/
│
├── backend/
│ ├── app/
│ │ ├── api/ # FastAPI routes (upload, chat, review, invoice)
│ │ ├── ingestion/ # File loading, OCR, parsing
│ │ ├── rag/ # Embeddings, vector store, routing
│ │ ├── database.py # SQLAlchemy models & DB session
│ │ ├── config.py # Environment & settings
│ │ └── main.py # FastAPI entry point
│ │
│ ├── .env.example
│ └── invoice_auditor.db # Created automatically (ignored in git)
│
├── ui/
│ └── streamlit_app.py # Streamlit frontend
│
├── data/
│ ├── uploads/ # Uploaded invoices (gitignored)
│ └── vector_db/ # FAISS vector stores (gitignored)
│
├── requirements.txt
├── .gitignore
└── README.md


---

## ⚙️ Prerequisites

- Python **3.9 or higher**
- At least **one LLM API key**
  - Cohere is recommended and works out of the box

---

## 🔑 Environment Setup

Create a `.env` file inside the `backend/` directory.

Example:

```env
# === REQUIRED (RECOMMENDED) ===
COHERE_API_KEY=your_cohere_api_key

# === OPTIONAL FALLBACKS ===
OPENAI_API_KEY=
GEMINI_API_KEY=

# === STORAGE PATHS ===
UPLOAD_PATH=../data/uploads
VECTOR_DB_PATH=../data/vector_db


📦 Installation

Clone the repository:

git clone https://github.com/shaileshthakur1/ai-invoice-auditor.git
cd invoice-auditor

📦 Installation

Clone the repository:

git clone https://github.com/your-username/invoice-auditor.git
cd invoice-auditor


Install dependencies:

pip install -r requirements.txt

▶️ Running the Application
1️⃣ Start the Backend (FastAPI)
cd backend
uvicorn app.main:app --reload


Backend runs at:

http://127.0.0.1:8000


Interactive API docs (Swagger):

http://127.0.0.1:8000/docs

2️⃣ Start the Frontend (Streamlit)

Open a new terminal:

cd ui
streamlit run streamlit_app.py


The UI will open automatically in your browser.

🧪 How to Use the App

Upload one or more invoices from the sidebar

Select an invoice from the invoice selector

Expand Extracted Invoice Information to review parsed fields

Open Review & Actions:

Approve the invoice

Reject the invoice

Edit any extracted field

Ask questions in the AI Assistant section

View previous questions in Query History (sidebar)

🧑‍⚖️ Human-in-the-Loop (HITL)

Invoices start in a PROCESSED state

A human can:

Approve (trustworthy)

Reject (invalid)

Edit extracted fields

Edited values are persisted in the database

AI answers always reflect the latest approved data

Flagged invoices warn users before answering

🧠 LLM & Embeddings Strategy

Default provider: Cohere (chat + embeddings)

Fallback providers: OpenAI, Gemini

Each invoice:

has its own FAISS vector store

is queried independently

This prevents cross-invoice context leakage

🚀 Why This Project Is Different

Deterministic extraction before LLM usage

Explicit human approval workflow

Audit-safe, explainable architecture

Clear separation of ingestion, storage, reasoning, and review

Designed as a verification workspace, not just a chatbot

📌 Possible Future Improvements

Role-based access (viewer vs reviewer)

Rule-based auto-flagging (business validations)

Exportable audit reports

Background processing / queues

Docker & cloud deployment

🧹 Git Hygiene

Runtime data is ignored (data/, databases, vector stores)

Secrets are never committed

Only reproducible code is versioned

📝 License

MIT License

