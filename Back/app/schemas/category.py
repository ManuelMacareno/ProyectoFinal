from pydantic import BaseModel

class CategoriaBase(BaseModel):
    nombre: str
    tipo: str  # "ingreso" o "gasto"

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int
    usuario_id: int

    class Config:
        from_attributes = True