import os
from langchain_mistralai import ChatMistralAI


def build_mistral_llm(temperature: float = 0.0) -> ChatMistralAI:
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise RuntimeError("MISTRAL_API_KEY environment variable not set")
    return ChatMistralAI(
        model="mistral-small-latest",
        temperature=temperature,
        mistral_api_key=api_key,
    )
