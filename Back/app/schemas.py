from pydantic import BaseModel
from typing import List, Optional
import datetime

# --- Esquemas para Transacciones ---

class TransaccionBase(BaseModel):
    monto: float
    descripcion: Optional[str] = None
    tipo: str # "ingreso" o "gasto"
    categoria_id: int

class TransaccionCreate(TransaccionBase):
    pass

class Transaccion(TransaccionBase):
    id: int
    fecha: datetime.datetime
    usuario_id: int

    class Config:
        from_attributes = True 

# --- Esquemas para Categorías ---

class CategoriaBase(BaseModel):
    nombre: str
    tipo: str # "ingreso" o "gasto"

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int
    usuario_id: int

    class Config:
        from_attributes = True 

# --- Esquemas para Usuarios ---

class UsuarioBase(BaseModel):
    email: str
    nombre: Optional[str] = None

class UsuarioCreate(UsuarioBase):
    password: str

class Usuario(UsuarioBase):
    id: int
    transacciones: List[Transaccion] = []
    categorias: List[Categoria] = []

    class Config:
        from_attributes = True 

# --- Esquemas para Autenticación (Tokens) ---

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class GastoCategoria(BaseModel):
    # Recharts espera 'name' y 'value' para el PieChart
    name: str
    value: float

class DashboardSummary(BaseModel):
    total_ingresos: float
    total_gastos: float
    balance: float
    gastos_por_categoria: List[GastoCategoria]

    class Config:
        from_attributes = True # (Era orm_mode, lo actualizamos)