from app.config import settings

# Cohere embeddings
from langchain_cohere import CohereEmbeddings

# Optional providers (future-proof)
# from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings


def get_embedding_model():
    """
    Select embedding model.
    Priority:
    1. Cohere (DEFAULT)
    2. OpenAI
    3. Gemini
    """

    # ✅ DEFAULT: Cohere
    if settings.COHERE_API_KEY:
        return CohereEmbeddings(
            model="embed-english-v3.0"
        )

    # Optional fallbacks
    if settings.OPENAI_API_KEY:
        return OpenAIEmbeddings(
            model="text-embedding-3-large"
        )

    if settings.GEMINI_API_KEY:
        return GoogleGenerativeAIEmbeddings(
            model="models/embedding-001"
        )

    raise RuntimeError(
        "No embedding provider available. Please set COHERE_API_KEY (recommended)."
    )
