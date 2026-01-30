from sqlalchemy.orm import Session
from sqlalchemy import func, extract, case
from datetime import datetime
from app.db.models import Transaccion, Categoria
from app.schemas.transaction import TransaccionCreate
from app.schemas.dashboard import DashboardSummary, GastoCategoria  # ¡Importar desde dashboard!

def get_transacciones(db: Session, usuario_id: int, skip: int = 0, limit: int = 100):
    return db.query(Transaccion).filter(
        Transaccion.usuario_id == usuario_id
    ).order_by(Transaccion.fecha.desc()).offset(skip).limit(limit).all()

def get_transaccion(db: Session, transaccion_id: int, usuario_id: int):
    return db.query(Transaccion).filter(
        Transaccion.id == transaccion_id,
        Transaccion.usuario_id == usuario_id
    ).first()

def create_user_transaccion(db: Session, transaccion: TransaccionCreate, usuario_id: int):
    categoria = db.query(Categoria).filter(
        Categoria.id == transaccion.categoria_id,
        Categoria.usuario_id == usuario_id
    ).first()
    if not categoria:
        return None
    db_transaccion = Transaccion(**transaccion.dict(), usuario_id=usuario_id)
    db.add(db_transaccion)
    db.commit()
    db.refresh(db_transaccion)
    return db_transaccion

def update_transaccion(db: Session, transaccion_id: int, transaccion: TransaccionCreate, usuario_id: int):
    db_transaccion = get_transaccion(db, transaccion_id, usuario_id)
    if not db_transaccion:
        return None
    transaccion_data = transaccion.dict()
    for key, value in transaccion_data.items():
        setattr(db_transaccion, key, value)
    db.add(db_transaccion)
    db.commit()
    db.refresh(db_transaccion)
    return db_transaccion

def delete_transaccion(db: Session, transaccion_id: int, usuario_id: int):
    db_transaccion = get_transaccion(db, transaccion_id, usuario_id)
    if not db_transaccion:
        return None
    db.delete(db_transaccion)
    db.commit()
    return db_transaccion

def get_dashboard_summary(db: Session, usuario_id: int):
    now = datetime.utcnow()
    current_month = now.month
    current_year = now.year

    total_ingresos = db.query(func.sum(Transaccion.monto)).filter(
        Transaccion.usuario_id == usuario_id,
        Transaccion.tipo == 'ingreso',
        extract('month', Transaccion.fecha) == current_month,
        extract('year', Transaccion.fecha) == current_year
    ).scalar() or 0.0

    total_gastos = db.query(func.sum(Transaccion.monto)).filter(
        Transaccion.usuario_id == usuario_id,
        Transaccion.tipo == 'gasto',
        extract('month', Transaccion.fecha) == current_month,
        extract('year', Transaccion.fecha) == current_year
    ).scalar() or 0.0

    gastos_categoria_query = db.query(
        Categoria.nombre,
        func.sum(Transaccion.monto).label('total')
    ).join(
        Categoria, Transaccion.categoria_id == Categoria.id
    ).filter(
        Transaccion.usuario_id == usuario_id,
        Transaccion.tipo == 'gasto',
        extract('month', Transaccion.fecha) == current_month,
        extract('year', Transaccion.fecha) == current_year
    ).group_by(Categoria.nombre).all()

    # Cambiar a List[GastoCategoria]
    gastos_por_categoria = [
        GastoCategoria(name=nombre, value=float(total)) 
        for nombre, total in gastos_categoria_query
    ]
    
    balance = total_ingresos - total_gastos

    return DashboardSummary(
        total_ingresos=float(total_ingresos),
        total_gastos=float(total_gastos),
        balance=float(balance),
        gastos_por_categoria=gastos_por_categoria
    )
    
    # Añade esto AL FINAL de app/db/crud/transaction.py

def obtener_balance_mensual(db: Session, usuario_id: int, año: int, mes: int):
    resultado = db.query(
        func.sum(
            case(
                (Transaccion.tipo == "ingreso", Transaccion.monto),
                else_=-Transaccion.monto
            )
        ).label("balance")
    ).filter(
        Transaccion.usuario_id == usuario_id,
        extract("year", Transaccion.fecha) == año,
        extract("month", Transaccion.fecha) == mes
    ).scalar()

    return float(resultado or 0.0)

def obtener_resumen_mensual(db: Session, usuario_id: int, año: int, mes: int):
    return db.query(
        Transaccion.categoria_id,
        func.sum(Transaccion.monto).label("total")
    ).filter(
        Transaccion.usuario_id == usuario_id,
        Transaccion.tipo == "gasto",
        extract("year", Transaccion.fecha) == año,
        extract("month", Transaccion.fecha) == mes
    ).group_by(Transaccion.categoria_id).all()