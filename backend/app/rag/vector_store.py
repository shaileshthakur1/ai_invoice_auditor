import os
from typing import List

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from app.config import settings
from app.rag.embedder import get_embedding_model


def create_vector_store(
    documents: List[Document],
    invoice_id: str
) -> FAISS:
    """
    Create and persist FAISS vector store for an invoice.
    """

    embeddings = get_embedding_model()

    invoice_path = os.path.join(
        settings.VECTOR_DB_PATH,
        invoice_id
    )

    os.makedirs(invoice_path, exist_ok=True)

    vector_store = FAISS.from_documents(
        documents,
        embeddings
    )

    vector_store.save_local(invoice_path)

    return vector_store


def load_vector_store(invoice_id: str) -> FAISS:
    """
    Load existing FAISS index from disk.
    """

    embeddings = get_embedding_model()

    invoice_path = os.path.join(
        settings.VECTOR_DB_PATH,
        invoice_id
    )

    if not os.path.exists(invoice_path):
        raise FileNotFoundError(
            f"No vector store found for invoice {invoice_id}"
        )

    return FAISS.load_local(
        invoice_path,
        embeddings,
        allow_dangerous_deserialization=True
    )
