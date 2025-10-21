from . import models, schemas, database
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Importamos 'models' y 'schemas' al inicio
from . import models, schemas

# --- Configuración de Seguridad ---
SECRET_KEY = "tu_clave_secreta_muy_larga_y_dificil"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # El token dura 30 minutos

# --- Contexto de Contraseña ÚNICO ---
# Esta es ahora la única definición de pwd_context en todo el proyecto.
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# Esquema de OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# --- Funciones de Autenticación ---

def verify_password(plain_password, hashed_password):
    """Verifica la contraseña plana contra el hash usando argon2."""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    """Crea un nuevo Token JWT."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- Dependencia para obtener el usuario actual ---

def get_current_user(
    db: Session = Depends(database.get_db), 
    token: str = Depends(oauth2_scheme)
):
    """
    Dependencia de FastAPI para proteger rutas.
    Decodifica el token, busca al usuario en la DB y lo devuelve.
    """
    
    # Importamos 'crud' aquí DENTRO para evitar importación circular
    from . import crud 
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub") # "sub" es el "subject" del token
        if email is None:
            raise credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    
    # Buscamos al usuario usando la función de crud
    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user