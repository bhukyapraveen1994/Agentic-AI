from typing import Literal

from langchain_openai import OpenAI
from langchain_ollama import Chatollama
from langchain_core_core,language_model import BaseChatModel

from .config import Settings
def get_llm(
        purpose: Literal["supervisor", "agent"] = "agent",
) -> BaseChatModel:
    """
    Return a Chat LLM instance based on env config.
    
    - purpose is just a hint; you could choose different models per role.
    """

    if settings.ll_provider == "openai":
        # OpenAI cloud model
        return OpenAI(
            api_key=settings.openai_api_key,
            model=settings.openai_model,
            temperature=0.2 if purpose == "supervisor" else 0.3,
        )
    

    # Default: ollama locale model
    return Chatollama(
        model=settings.olama_model,
        temperature=0.2 if purpose == "supervisor" else 0.3,
    )
