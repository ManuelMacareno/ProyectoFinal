from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from starlette.responses import Response
from starlette import status

from app import crud, schemas, models
from app.api.deps import get_db, get_current_user

router = APIRouter(prefix="/categorias", tags=["Categorías"])

@router.post("/", response_model=schemas.Categoria)
def crear_categoria(
    categoria: schemas.CategoriaCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user),
):
    return crud.create_user_categoria(db=db, categoria=categoria, usuario_id=current_user.id)

@router.get("/", response_model=List[schemas.Categoria])
def leer_categorias_usuario(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user),
):
    return crud.get_categorias(db, usuario_id=current_user.id, skip=skip, limit=limit)

@router.put("/{categoria_id}", response_model=schemas.Categoria)
def actualizar_categoria(
    categoria_id: int,
    categoria: schemas.CategoriaCreate,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user),
):
    db_categoria = crud.update_categoria(db, categoria_id=categoria_id, categoria=categoria, usuario_id=current_user.id)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_categoria

@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_categoria(
    categoria_id: int,
    db: Session = Depends(get_db),
    current_user: models.Usuario = Depends(get_current_user),
):
    res = crud.delete_categoria(db, categoria_id=categoria_id, usuario_id=current_user.id)
    if res is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    if res == "EN_USO":
        raise HTTPException(status_code=400, detail="No se puede borrar la categoría porque tiene transacciones asociadas.")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
