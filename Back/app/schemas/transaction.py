from pydantic import BaseModel
from typing import Optional
import datetime

class TransaccionBase(BaseModel):
    monto: float
    descripcion: Optional[str] = None
    tipo: str  # "ingreso" o "gasto"
    categoria_id: int

class TransaccionCreate(TransaccionBase):
    pass

class Transaccion(TransaccionBase):
    id: int
    fecha: datetime.datetime
    usuario_id: int

    class Config:
        from_attributes = True