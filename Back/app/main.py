from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from starlette.responses import Response 
from . import crud, models, schemas, auth, database
from starlette import status             

from . import crud, models, schemas, auth

# --- Configuración de la App y Base de Datos ---
app = FastAPI(title="Gestor de Gastos API")

# --- Configuración de CORS ---
origins = [
    "http://localhost:5173", # La URL de tu frontend con Vite
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Permite estos orígenes
    allow_credentials=True,    # Permite credenciales
    allow_methods=["*"],         # Permite todos los métodos (POST, GET, etc.)
    allow_headers=["*"],         # Permite todos los headers
)

# Llama a la función de models.py para crear las tablas
models.crear_db() 


# --- Endpoints de Autenticación y Usuarios ---

@app.post("/usuarios/", response_model=schemas.Usuario, tags=["Usuarios"])
def crear_usuario(user: schemas.UsuarioCreate, db: Session = Depends(database.get_db)):
    """
    Registra un nuevo usuario en la base de datos.
    """
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.Token, tags=["Usuarios"])
def login_para_access_token(
    db: Session = Depends(database.get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
):
    # --- DEBUGGING ---
    print("\n--- INTENTANDO LOGIN ---")
    print(f"Dato recibido (form_data.username): {form_data.username}")
    print(f"Password recibido: {form_data.password}")
    # --- FIN DEBUGGING ---

    user = crud.get_user_by_email_or_username(db, username_or_email=form_data.username)

    # --- DEBUGGING ---
    if user:
        print(f"Usuario encontrado en DB: {user.nombre} (Email: {user.email})")
        es_valido = auth.verify_password(form_data.password, user.hashed_password)
        print(f"Verificación de contraseña: {es_valido}")
    else:
        print("Resultado de la búsqueda: Usuario NO encontrado.")
    print("------------------------\n")
    # --- FIN DEBUGGING ---

    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email/Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token(
        data={"sub": user.email}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/usuarios/me/", response_model=schemas.Usuario, tags=["Usuarios"])
def leer_usuario_actual(
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    """
    Devuelve la información del usuario que está logueado (autenticado).
    """
    return current_user

# --- Endpoints de Categorías ---

@app.post("/categorias/", response_model=schemas.Categoria, tags=["Categorías"])
def crear_categoria(
    categoria: schemas.CategoriaCreate, 
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    """
    Crea una nueva categoría para el usuario logueado.
    """
    return crud.create_user_categoria(db=db, categoria=categoria, usuario_id=current_user.id)

@app.get("/categorias/", response_model=List[schemas.Categoria], tags=["Categorías"])
def leer_categorias_usuario(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    """
    Obtiene la lista de categorías creadas por el usuario logueado.
    """
    categorias = crud.get_categorias(db, usuario_id=current_user.id, skip=skip, limit=limit)
    return categorias

@app.put("/categorias/{categoria_id}", response_model=schemas.Categoria, tags=["Categorías"])
def actualizar_categoria(
    categoria_id: int,
    categoria: schemas.CategoriaCreate,
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    """
    Actualiza una categoría existente.
    """
    db_categoria = crud.update_categoria(
        db, 
        categoria_id=categoria_id, 
        categoria=categoria, 
        usuario_id=current_user.id
    )
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_categoria


@app.delete("/categorias/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Categorías"])
def eliminar_categoria(
    categoria_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    """
    Borra una categoría.
    """
    db_categoria = crud.delete_categoria(db, categoria_id=categoria_id, usuario_id=current_user.id)
    
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    
    if db_categoria == "EN_USO":
        # Error 400 (Bad Request) porque el usuario intentó algo inválido
        raise HTTPException(status_code=400, detail="No se puede borrar la categoría porque tiene transacciones asociadas.")
        
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# --- Endpoints de Transacciones ---

@app.post("/transacciones/", response_model=schemas.Transaccion, tags=["Transacciones"])
def crear_transaccion(
    transaccion: schemas.TransaccionCreate,
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    """
    Crea una nueva transacción (gasto o ingreso) para el usuario logueado.
    """
    db_transaccion = crud.create_user_transaccion(db=db, transaccion=transaccion, usuario_id=current_user.id)
    if db_transaccion is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada o no pertenece al usuario")
    return db_transaccion

@app.get("/transacciones/", response_model=List[schemas.Transaccion], tags=["Transacciones"])
def leer_transacciones_usuario(
    skip: int = 0, limit: int = 100,
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    """
    Obtiene la lista de transacciones del usuario logueado, ordenadas por fecha.
    """
    transacciones = crud.get_transacciones(db, usuario_id=current_user.id, skip=skip, limit=limit)
    return transacciones

@app.put("/transacciones/{transaccion_id}", response_model=schemas.Transaccion, tags=["Transacciones"])
def actualizar_transaccion(
    transaccion_id: int,
    transaccion: schemas.TransaccionCreate,
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    """
    Actualiza una transacción existente (RF-006).
    """
    db_transaccion = crud.update_transaccion(
        db, 
        transaccion_id=transaccion_id, 
        transaccion=transaccion, 
        usuario_id=current_user.id
    )
    if db_transaccion is None:
        raise HTTPException(status_code=404, detail="Transacción no encontrada o no pertenece al usuario")
    return db_transaccion


@app.delete("/transacciones/{transaccion_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Transacciones"])
def eliminar_transaccion(
    transaccion_id: int,
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    """
    Borra una transacción (RF-007).
    """
    db_transaccion = crud.delete_transaccion(db, transaccion_id=transaccion_id, usuario_id=current_user.id)
    if db_transaccion is None:
        raise HTTPException(status_code=404, detail="Transacción no encontrada o no pertenece al usuario")

    # HTTP 204 significa "OK, lo borré, no devuelvo contenido"
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# --- Endpoint de Dashboard ---
@app.get("/dashboard/summary", response_model=schemas.DashboardSummary, tags=["Dashboard"])
def get_summary(
    db: Session = Depends(database.get_db),
    current_user: models.Usuario = Depends(auth.get_current_user)
):
    """
    Obtiene el resumen del dashboard para el mes actual (RF-010, RF-011).
    """
    return crud.get_dashboard_summary(db=db, usuario_id=current_user.id)