import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    UPLOAD_PATH = os.getenv(
        "UPLOAD_PATH",
        os.path.join(BASE_DIR, "../data/uploads")
    )

    VECTOR_DB_PATH = os.getenv(
        "VECTOR_DB_PATH",
        os.path.join(BASE_DIR, "../data/vector_db")
    )

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")

    BEDROCK_AWS_ACCESS_KEY = os.getenv("BEDROCK_AWS_ACCESS_KEY")
    BEDROCK_AWS_SECRET_KEY = os.getenv("BEDROCK_AWS_SECRET_KEY")
    BEDROCK_REGION = os.getenv("BEDROCK_REGION")

    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")


settings = Settings()
