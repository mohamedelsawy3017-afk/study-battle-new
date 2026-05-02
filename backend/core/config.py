# core/config.py - App configuration & settings
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Study Battle"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "study-battle-super-secret-key-change-in-production-2024")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./study_battle.db")
    
    # Convert Railway's PostgreSQL URL to async format
    if DATABASE_URL and "postgresql://" in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif DATABASE_URL and "postgres://" in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

    class Config:
        env_file = ".env"


settings = Settings()