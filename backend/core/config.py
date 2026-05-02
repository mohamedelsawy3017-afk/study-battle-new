# core/config.py - App configuration & settings
from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Study Battle"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False  # Set to False in production!

    # JWT
    SECRET_KEY: str = os.getenv("SECRET_KEY", "study-battle-super-secret-key-change-in-production-2024")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Database - Railway will provide DATABASE_URL
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./study_battle.db")
    
    # If using PostgreSQL (Railway auto-sets this), convert asyncpg:// to postgresql+asyncpg://
    if DATABASE_URL and DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

    class Config:
        env_file = ".env"


settings = Settings()