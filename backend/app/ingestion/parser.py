import re


def normalize_text(text: str) -> str:
    """
    Clean invoice text for better embeddings & retrieval.
    """

    text = re.sub(r"\s+", " ", text)

    text = re.sub(r"[^\x00-\x7F]+", " ", text)

    return text.strip()
