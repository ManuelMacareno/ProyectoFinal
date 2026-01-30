from sqlalchemy.orm import Session
from app.db.models import Categoria, Transaccion
from app.schemas.category import CategoriaCreate

def get_categorias(db: Session, usuario_id: int, skip: int = 0, limit: int = 100):
    return db.query(Categoria).filter(
        Categoria.usuario_id == usuario_id
    ).offset(skip).limit(limit).all()

def get_categoria(db: Session, categoria_id: int, usuario_id: int):
    return db.query(Categoria).filter(
        Categoria.id == categoria_id,
        Categoria.usuario_id == usuario_id
    ).first()

def create_user_categoria(db: Session, categoria: CategoriaCreate, usuario_id: int):
    db_categoria = Categoria(**categoria.dict(), usuario_id=usuario_id)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def update_categoria(db: Session, categoria_id: int, categoria: CategoriaCreate, usuario_id: int):
    db_categoria = get_categoria(db, categoria_id, usuario_id)
    if not db_categoria:
        return None
    db_categoria.nombre = categoria.nombre
    db_categoria.tipo = categoria.tipo
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def delete_categoria(db: Session, categoria_id: int, usuario_id: int):
    db_categoria = get_categoria(db, categoria_id, usuario_id)
    if not db_categoria:
        return None
    transacciones_en_uso = db.query(Transaccion).filter(
        Transaccion.categoria_id == categoria_id
    ).first()
    if transacciones_en_uso:
        return "EN_USO"
    db.delete(db_categoria)
    db.commit()
    return db_categoria