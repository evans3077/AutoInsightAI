import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

class Settings:
    APP_NAME: str = "AutoInsightAI"
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    DATABASE_URL: str = f"sqlite:///{BASE_DIR}/data/autoinsightai.db"

settings = Settings()
