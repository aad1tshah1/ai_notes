import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    anthropic_model: str = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5")
    anthropic_max_tokens: int = int(os.getenv("ANTHROPIC_MAX_TOKENS", "1024"))
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")

    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    def __init__(self):
        if not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")


config = Config()
