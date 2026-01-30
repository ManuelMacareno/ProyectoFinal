# app/db/init_db.py
from app.db.database import Base, engine
from app.db import models  # <-- este es el correcto

def init_db() -> None:
    Base.metadata.create_all(bind=engine)
