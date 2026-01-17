from typing import List
from uuid import uuid4

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.rag.vector_store import create_vector_store


def chunk_and_store(
    text: str,
    invoice_id: str
):
    """
    Split invoice text into chunks and store embeddings.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_text(text)

    documents: List[Document] = []

    for i, chunk in enumerate(chunks):
        documents.append(
            Document(
                page_content=chunk,
                metadata={
                    "invoice_id": invoice_id,
                    "chunk_id": str(uuid4()),
                    "chunk_index": i
                }
            )
        )

    return create_vector_store(documents, invoice_id)
