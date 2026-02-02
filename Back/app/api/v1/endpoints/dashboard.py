# app/api/endpoints/dashboard.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.db.database import get_db
from app.api.deps import get_current_user
from app.db.models import Usuario
from app.db.crud.transaction import get_dashboard_summary

from app.schemas.dashboard import DashboardSummary
from app.db.models import Transaccion, Categoria
from sqlalchemy import func, extract

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

# 1. Resumen COMPLETO del mes actual (el que ya tenías funcionando)
@router.get("/", response_model=DashboardSummary)
def obtener_resumen_actual(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    """
    Resumen completo del mes actual:
    - Total ingresos
    - Total gastos  
    - Balance neto
    - Gastos por categoría (para gráficos)
    """
    return get_dashboard_summary(db, usuario_id=current_user.id)

# 2. Balance específico por mes (NUEVO - complementario)
@router.get("/balance/{year}/{month}")
def obtener_balance_mensual_endpoint(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="El mes debe estar entre 1 y 12")

    total_ingresos = db.query(func.sum(Transaccion.monto)).filter(
        Transaccion.usuario_id == current_user.id,
        Transaccion.tipo == "ingreso",
        extract("year", Transaccion.fecha) == year,
        extract("month", Transaccion.fecha) == month,
    ).scalar() or 0

    total_gastos = db.query(func.sum(Transaccion.monto)).filter(
        Transaccion.usuario_id == current_user.id,
        Transaccion.tipo == "gasto",
        extract("year", Transaccion.fecha) == year,
        extract("month", Transaccion.fecha) == month,
    ).scalar() or 0

    balance = total_ingresos - total_gastos

    return {
        "year": year,
        "month": month,
        "total_ingresos": float(total_ingresos),
        "total_gastos": float(total_gastos),
        "balance": float(balance),
    }

# 3. Resumen por categoría para un mes específico (NUEVO)
@router.get("/resumen/{year}/{month}")
def obtener_resumen_mensual_endpoint(
    year: int,
    month: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    if month < 1 or month > 12:
        raise HTTPException(status_code=400, detail="El mes debe estar entre 1 y 12")

    rows = (
        db.query(
            Categoria.id.label("categoria_id"),
            Categoria.nombre.label("nombre"),
            func.sum(Transaccion.monto).label("total"),
        )
        .join(Categoria, Categoria.id == Transaccion.categoria_id)
        .filter(
            Transaccion.usuario_id == current_user.id,
            Transaccion.tipo == "gasto",  # <-- CLAVE: solo gastos
            extract("year", Transaccion.fecha) == year,
            extract("month", Transaccion.fecha) == month,
        )
        .group_by(Categoria.id, Categoria.nombre)
        .all()
    )

    return {
        "year": year,
        "month": month,
        "resumen_por_categoria": [
            {"categoria_id": r.categoria_id, "nombre": r.nombre, "total": float(r.total or 0)}
            for r in rows
        ],
    }
    
# 4. Balance del mes actual (alternativa simple)
@router.get("/balance-actual")
def obtener_balance_actual(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user),
):
    ahora = datetime.utcnow()
    año = ahora.year
    mes = ahora.month

    # Total ingresos
    total_ingresos = db.query(func.sum(Transaccion.monto)).filter(
        Transaccion.usuario_id == current_user.id,
        Transaccion.tipo == "ingreso",
        extract("year", Transaccion.fecha) == año,
        extract("month", Transaccion.fecha) == mes,
    ).scalar() or 0

    # Total gastos
    total_gastos = db.query(func.sum(Transaccion.monto)).filter(
        Transaccion.usuario_id == current_user.id,
        Transaccion.tipo == "gasto",
        extract("year", Transaccion.fecha) == año,
        extract("month", Transaccion.fecha) == mes,
    ).scalar() or 0

    balance = total_ingresos - total_gastos

    return {
        "total_ingresos": total_ingresos,
        "total_gastos": total_gastos,
        "balance": balance,
        "year": año,
        "month": mes,
    }