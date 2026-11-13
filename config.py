"""Environment-based configuration."""

import os

from dotenv import load_dotenv
from langchain_ollama import ChatOllama


load_dotenv()


def create_chat_model() -> ChatOllama:
    """Create the configured local chat model."""
    return ChatOllama(
        model=os.getenv("OLLAMA_MODEL", "llama3.1:8b"),
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        temperature=0,
    )
