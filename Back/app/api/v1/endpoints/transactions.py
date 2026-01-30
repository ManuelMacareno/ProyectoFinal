from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from starlette.responses import Response
from starlette import status

from app.db.database import get_db
from app.api.deps import get_current_user
from app.db.models import Usuario
from app.schemas.transaction import Transaccion, TransaccionCreate
from app.db.crud.transaction import (
    create_user_transaccion,
    get_transacciones,
    get_transaccion,
    update_transaccion,
    delete_transaccion
)

router = APIRouter(prefix="/transacciones", tags=["Transacciones"])

@router.post("/", response_model=Transaccion)
def crear_transaccion(
    transaccion: TransaccionCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    db_transaccion = create_user_transaccion(
        db=db, 
        transaccion=transaccion,  # ¡NO usar .dict() aquí! El CRUD ya lo hace
        usuario_id=current_user.id
    )
    if db_transaccion is None:
        raise HTTPException(
            status_code=404, 
            detail="Categoría no encontrada o no pertenece al usuario"
        )
    return db_transaccion

@router.get("/", response_model=List[Transaccion])
def leer_transacciones_usuario(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    return get_transacciones(
        db, 
        usuario_id=current_user.id, 
        skip=skip, 
        limit=limit
    )

@router.put("/{transaccion_id}", response_model=Transaccion)
def actualizar_transaccion_endpoint(
    transaccion_id: int,
    transaccion: TransaccionCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    db_transaccion = update_transaccion(
        db,
        transaccion_id=transaccion_id,
        transaccion=transaccion,
        usuario_id=current_user.id,
    )
    if db_transaccion is None:
        raise HTTPException(
            status_code=404, 
            detail="Transacción no encontrada o no pertenece al usuario"
        )
    return db_transaccion

@router.delete("/{transaccion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_transaccion_endpoint(
    transaccion_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    success = delete_transaccion(db, transaccion_id=transaccion_id, usuario_id=current_user.id)
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Transacción no encontrada o no pertenece al usuario"
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)