# app/db/init_db.py
from app.database import Base, engine
import app.models  # importante: registra los modelos en Base.metadata

def init_db() -> None:
    Base.metadata.create_all(bind=engine)
