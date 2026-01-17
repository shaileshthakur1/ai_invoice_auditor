from typing import List

from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate

from app.llm_fallback import safe_llm_invoke


QA_PROMPT = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are an invoice auditing assistant.

Rules:
1. First, try to answer STRICTLY using the provided invoice context.
2. If the answer is NOT present in the invoice context:
   - Provide the best possible answer using your general knowledge.
   - On the NEXT LINE, clearly notify the user with EXACTLY:
     "⚠️ The relevant information was not found in the invoice. This answer is based on general knowledge."

Additional constraints:
- Be precise and factual.
- Do NOT fabricate invoice-specific numbers or entities.
- Do NOT calculate invoice values unless explicitly stated in the context.

Invoice Context:
{context}

Question:
{question}

Answer:
"""
)


def format_context(documents: List[Document]) -> str:
    """
    Combine retrieved documents into a single context string.
    """
    return "\n\n".join(
        f"- {doc.page_content}" for doc in documents
    )


def answer_question(
    documents: List[Document],
    question: str
) -> str:
    """
    Generate grounded answer using retrieved context.
    """

    context = format_context(documents)

    prompt = QA_PROMPT.format(
        context=context,
        question=question
    )

    return safe_llm_invoke(prompt)
