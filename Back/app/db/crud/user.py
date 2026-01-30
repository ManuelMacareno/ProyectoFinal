# app/db/crud/user.py (VERSIÓN COMPLETA)
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from app.db.models import Usuario
from app.schemas.user import UsuarioCreate
from app.core.security import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(Usuario).filter(func.lower(Usuario.email) == email.lower()).first()

def get_user_by_email_or_username(db: Session, username_or_email: str):
    """Busca por email O nombre (para login flexible)"""
    search_term = username_or_email.lower()
    return db.query(Usuario).filter(
        or_(
            func.lower(Usuario.email) == search_term,
            func.lower(Usuario.nombre) == search_term
        )
    ).first()

def create_user(db: Session, user: UsuarioCreate):
    hashed_password = get_password_hash(user.password)
    db_user = Usuario(
        email=user.email.lower(),
        nombre=user.nombre.lower(),
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user