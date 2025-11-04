from decouple import config
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # JWT Settings
    SECRET_KEY: str = config("SECRET_KEY", default="your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: str = config("DATABASE_URL", default="sqlite:///./data/autoinsightai.db")
    
    # Redis for task queue
    REDIS_URL: str = config("REDIS_URL", default="redis://localhost:6379")
    
    # Model Server
    MODEL_SERVER_URL: str = config("MODEL_SERVER_URL", default="http://localhost:8001")
    
    # YouTube API (for future TPE)
    YOUTUBE_API_KEY: str = config("YOUTUBE_API_KEY", default="")

settings = Settings()