from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.api.deps import get_current_user
from app.db.models import Usuario
from app.schemas.user import Usuario, UsuarioCreate
from app.db.crud.user import get_user_by_email, create_user

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/", response_model=Usuario)
def crear_usuario(user: UsuarioCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    return create_user(db=db, user=user)

@router.get("/me/", response_model=Usuario)
def leer_usuario_actual(current_user: Usuario = Depends(get_current_user)):
    return current_user