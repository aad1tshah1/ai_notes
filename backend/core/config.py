import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    anthropic_model: str = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5")
    anthropic_max_tokens: int = int(os.getenv("ANTHROPIC_MAX_TOKENS", "1024"))
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    secret_key:str = os.getenv("SECRET_KEY")
    algorithm:str = os.getenv("ALGORITHM")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

    debug: bool = os.getenv("DEBUG", "False").lower() == "true"

    def __init__(self):
        if not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")

        if not self.secret_key:
            raise ValueError("SECRET_KEY environment variable is required")

        if not self.algorithm:
            raise ValueError("ALGORITHM environment variable is required")


config = Config()
