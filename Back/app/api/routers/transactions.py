from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from starlette.responses import Response
from starlette import status

from app import crud, schemas, models
from app.api.deps import get_db, get_current_user

router = APIRouter(prefix="/transacciones", tags=["Transacciones"])

@router.post("/", response_model=schemas.Transaccion)
def crear_transaccion(
    transaccion: schemas.TransaccionCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user),
):
    db_transaccion = crud.create_user_transaccion(db=db, transaccion=transaccion, usuario_id=current_user.id)
    if db_transaccion is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada o no pertenece al usuario")
    return db_transaccion

@router.get("/", response_model=List[schemas.Transaccion])
def leer_transacciones_usuario(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user),
):
    return crud.get_transacciones(db, usuario_id=current_user.id, skip=skip, limit=limit)

@router.put("/{transaccion_id}", response_model=schemas.Transaccion)
def actualizar_transaccion(
    transaccion_id: int,
    transaccion: schemas.TransaccionCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user),
):
    db_transaccion = crud.update_transaccion(
        db,
        transaccion_id=transaccion_id,
        transaccion=transaccion,
        usuario_id=current_user.id,
    )
    if db_transaccion is None:
        raise HTTPException(status_code=404, detail="Transacción no encontrada o no pertenece al usuario")
    return db_transaccion

@router.delete("/{transaccion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_transaccion(
    transaccion_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user),
):
    db_transaccion = crud.delete_transaccion(db, transaccion_id=transaccion_id, usuario_id=current_user.id)
    if db_transaccion is None:
        raise HTTPException(status_code=404, detail="Transacción no encontrada o no pertenece al usuario")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
