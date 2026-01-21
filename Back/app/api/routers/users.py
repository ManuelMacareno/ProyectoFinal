from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas, models, auth
from app.api.deps import get_db

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.post("/", response_model=schemas.Usuario)
def crear_usuario(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    return crud.create_user(db=db, user=user)

@router.get("/me/", response_model=schemas.Usuario)
def leer_usuario_actual(current_user: models.Usuario = Depends(auth.get_current_user)):
    return current_user
