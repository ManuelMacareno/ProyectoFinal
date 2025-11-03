from sqlalchemy.orm import Session
from passlib.context import CryptContext  # Importante para hashear passwords
from sqlalchemy import func, extract, or_
from datetime import datetime
from . import models, schemas
from . import auth

# Configuración para hashear contraseñas
pwd_context = auth.pwd_context

# --- CRUD de Usuarios ---

def get_user_by_email(db: Session, email: str):
    return db.query(models.Usuario).filter(func.lower(models.Usuario.email) == email.lower()).first()

def hash_password(password: str):
    return pwd_context.hash(password)

def create_user(db: Session, user: schemas.UsuarioCreate):
    hashed_password = hash_password(user.password)
    # --- DEBUGGING ---
    print("\n--- REGISTRANDO USUARIO ---")
    print(f"Email Original: {user.email} -> Guardado como: {user.email.lower()}")
    print(f"Nombre Original: {user.nombre} -> Guardado como: {user.nombre.lower()}")
    print("--------------------------")
    # --- FIN DEBUGGING ---
    db_user = models.Usuario(
        email=user.email.lower(),       
        nombre=user.nombre.lower(),    
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- CRUD de Categorías ---

def get_categorias(db: Session, usuario_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Categoria).filter(
        models.Categoria.usuario_id == usuario_id
    ).offset(skip).limit(limit).all()

def create_user_categoria(db: Session, categoria: schemas.CategoriaCreate, usuario_id: int):
    db_categoria = models.Categoria(**categoria.dict(), usuario_id=usuario_id)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def get_categoria(db: Session, categoria_id: int, usuario_id: int):
    """
    Helper: Obtiene una sola categoría, verificando que pertenezca al usuario.
    """
    return db.query(models.Categoria).filter(
        models.Categoria.id == categoria_id,
        models.Categoria.usuario_id == usuario_id
    ).first()

def update_categoria(db: Session, categoria_id: int, categoria: schemas.CategoriaCreate, usuario_id: int):
    """
    Actualiza una categoría.
    """
    db_categoria = get_categoria(db, categoria_id, usuario_id)
    if not db_categoria:
        return None
    
    # Actualizamos los campos
    db_categoria.nombre = categoria.nombre
    db_categoria.tipo = categoria.tipo
    
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def delete_categoria(db: Session, categoria_id: int, usuario_id: int):
    """
    Borra una categoría.
    """
    db_categoria = get_categoria(db, categoria_id, usuario_id)
    if not db_categoria:
        return None
    
    # VALIDACIÓN: No dejar borrar categoría si está en uso
    transacciones_en_uso = db.query(models.Transaccion).filter(
        models.Transaccion.categoria_id == categoria_id
    ).first()
    
    if transacciones_en_uso:
        # No podemos borrarla, levantamos un error
        return "EN_USO"

    db.delete(db_categoria)
    db.commit()
    return db_categoria

# --- CRUD de Transacciones ---

def get_transacciones(db: Session, usuario_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Transaccion).filter(
        models.Transaccion.usuario_id == usuario_id
    ).order_by(models.Transaccion.fecha.desc()).offset(skip).limit(limit).all()

def create_user_transaccion(db: Session, transaccion: schemas.TransaccionCreate, usuario_id: int):
    # Verificación de seguridad: que la categoría pertenezca al usuario
    categoria = db.query(models.Categoria).filter(
        models.Categoria.id == transaccion.categoria_id,
        models.Categoria.usuario_id == usuario_id
    ).first()
    
    if not categoria:
        return None # O lanzar una excepción

    db_transaccion = models.Transaccion(
        **transaccion.dict(), 
        usuario_id=usuario_id
    )
    db.add(db_transaccion)
    db.commit()
    db.refresh(db_transaccion)
    return db_transaccion

def get_transaccion(db: Session, transaccion_id: int, usuario_id: int):
    """
    Helper: Obtiene una sola transacción, verificando que pertenezca al usuario.
    """
    return db.query(models.Transaccion).filter(
        models.Transaccion.id == transaccion_id,
        models.Transaccion.usuario_id == usuario_id
    ).first()

def update_transaccion(db: Session, transaccion_id: int, transaccion: schemas.TransaccionCreate, usuario_id: int):
    """
    Actualiza una transacción. Reutilizamos el schema TransaccionCreate.
    """
    db_transaccion = get_transaccion(db, transaccion_id, usuario_id)
    if not db_transaccion:
        return None
    
    # Obtenemos los datos del schema
    transaccion_data = transaccion.dict()
    
    # Actualizamos los campos
    for key, value in transaccion_data.items():
        setattr(db_transaccion, key, value)
    
    db.add(db_transaccion)
    db.commit()
    db.refresh(db_transaccion)
    return db_transaccion

def delete_transaccion(db: Session, transaccion_id: int, usuario_id: int):
    """
    Borra una transacción.
    """
    db_transaccion = get_transaccion(db, transaccion_id, usuario_id)
    if not db_transaccion:
        return None
    
    db.delete(db_transaccion)
    db.commit()
    return db_transaccion # Devolvemos el objeto borrado (opcional)

def get_dashboard_summary(db: Session, usuario_id: int):
    # 1. Obtener mes y año actual
    now = datetime.utcnow()
    current_month = now.month
    current_year = now.year

    # 2. Calcular Total Ingresos (RF-010)
    total_ingresos = db.query(func.sum(models.Transaccion.monto)).filter(
        models.Transaccion.usuario_id == usuario_id,
        models.Transaccion.tipo == 'ingreso',
        extract('month', models.Transaccion.fecha) == current_month,
        extract('year', models.Transaccion.fecha) == current_year
    ).scalar() or 0.0 # .scalar() devuelve un solo valor, or 0.0 si es None

    # 3. Calcular Total Gastos (RF-010)
    total_gastos = db.query(func.sum(models.Transaccion.monto)).filter(
        models.Transaccion.usuario_id == usuario_id,
        models.Transaccion.tipo == 'gasto',
        extract('month', models.Transaccion.fecha) == current_month,
        extract('year', models.Transaccion.fecha) == current_year
    ).scalar() or 0.0

    # 4. Calcular Gastos por Categoría (RF-011)
    gastos_categoria_query = db.query(
        models.Categoria.nombre, # Queremos el nombre de la categoría
        func.sum(models.Transaccion.monto).label('total') # La suma
    ).join(
        models.Categoria, models.Transaccion.categoria_id == models.Categoria.id
    ).filter(
        models.Transaccion.usuario_id == usuario_id,
        models.Transaccion.tipo == 'gasto',
        extract('month', models.Transaccion.fecha) == current_month,
        extract('year', models.Transaccion.fecha) == current_year
    ).group_by(
        models.Categoria.nombre # Agrupamos por nombre
    ).all()

    # 5. Formatear los datos para el schema (y para Recharts)
    gastos_por_categoria = [
        {"name": nombre, "value": total} for nombre, total in gastos_categoria_query
    ]
    
    # 6. Calcular Balance (RF-010)
    balance = total_ingresos - total_gastos

    # Devolvemos el objeto que definimos en el schema
    return schemas.DashboardSummary(
        total_ingresos=total_ingresos,
        total_gastos=total_gastos,
        balance=balance,
        gastos_por_categoria=gastos_por_categoria
    )

def get_user_by_email_or_username(db: Session, username_or_email: str):
    """
    Busca un usuario por su email O por su nombre de usuario (nombre),
    de forma case-insensitive.
    """
    search_term = username_or_email.lower() # Convertimos el input a minúsculas
    # --- DEBUGGING ---
    print("\n--- BUSCANDO USUARIO ---")
    print(f"Término de búsqueda (original): {username_or_email}")
    print(f"Término de búsqueda (lowercase): {search_term}")
    # --- FIN DEBUGGING ---
    return db.query(models.Usuario).filter(
        or_(
            # Comparamos la columna de email en minúsculas con el input en minúsculas
            func.lower(models.Usuario.email) == search_term,
            # Comparamos la columna de nombre en minúsculas con el input en minúsculas
            func.lower(models.Usuario.nombre) == search_term
        )
    ).first()