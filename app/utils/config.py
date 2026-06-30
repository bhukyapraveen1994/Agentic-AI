import os 
from dotenv import load_dotenv

#load environment variables from .env file
load_dotenv()

class Settings:
    """Simple config holder for app-wide settings. """
    
    def __init__(self) -> None:
        self.app_name = os.getenv("APP_NAME", "Package tracking Assistant")
        self.app_env = os.getenv("APP_ENV", "dev")


        ##LLM providerr: "openai" or "ollama"
        self.llm_provider = os.getenv("LLM_PROVIDER", "ollama")

        #OpenAI config
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-40-mini")

        #ollama config
        self.olama_model = os.getenv("OLLAMA_MODEL", "llama3")

        settings = Settings()
        