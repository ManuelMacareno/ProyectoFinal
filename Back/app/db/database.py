# app/db/database.py
from app.core.config import settings

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# 1. Configuración del motor de base de datos
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Función get_db que FALTA (añádela)
def get_db():
    """
    Dependencia para obtener sesión de base de datos.
    FastAPI la usará automáticamente en los endpoints.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        