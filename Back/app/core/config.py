# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./gastos.db"
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    APP_NAME: str = "Gestor de Gastos API"
    CORS_ORIGINS: List[str] = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]


    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()
