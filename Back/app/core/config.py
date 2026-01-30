# app/core/config.py
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # 1. DATABASE_URL: Se lee desde .env. Si no existe, usamos SQLite.
    DATABASE_URL: str = "sqlite:///./gastos.db"
    
    # 2. SECRET_KEY: OBLIGATORIO desde .env. No tiene valor por defecto aquí.
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 3. Otros ajustes
    APP_NAME: str = "Gestor de Gastos API"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    class Config:
        env_file = ".env"  # Pydantic buscará las variables aquí

settings = Settings()