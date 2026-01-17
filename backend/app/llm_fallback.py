from typing import List

from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_cohere import ChatCohere
from langchain_community.llms import Ollama
from langchain_community.chat_models import BedrockChat

from app.config import settings


def get_llm_chain() -> List:
    """
    Returns a list of initialized LLMs.
    The system will try each one in order until one succeeds.
    """

    llms = []

 # 1. Cohere (DEFAULT)
    if settings.COHERE_API_KEY:
        try:
            llms.append(
                ChatCohere(
                    temperature=0
                )
            )
        except Exception:
            pass

    # 2. OpenAI
    if settings.OPENAI_API_KEY:
        try:
            llms.append(
                ChatOpenAI(
                    temperature=0,
                    model="gpt-4o-mini"
                )
            )
        except Exception:
            pass

    # 3. Gemini
    if settings.GEMINI_API_KEY:
        try:
            llms.append(
                ChatGoogleGenerativeAI(
                    model="gemini-pro",
                    temperature=0
                )
            )
        except Exception:
            pass

    if not llms:
        raise RuntimeError(
            "No LLM available. Please configure at least one API key."
        )

    return llms


def safe_llm_invoke(prompt: str) -> str:
    """
    Try invoking LLMs one by one.
    If one fails, move to the next.
    """

    llms = get_llm_chain()
    last_error = None

    for llm in llms:
        try:
            response = llm.invoke(prompt)
            return response.content
        except Exception as e:
            last_error = e
            continue

    raise RuntimeError(
        f"All LLM providers failed. Last error: {last_error}"
    )
