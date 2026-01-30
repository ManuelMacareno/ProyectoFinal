from pydantic import BaseModel
from typing import List

class GastoCategoria(BaseModel):
    name: str
    value: float

class DashboardSummary(BaseModel):
    total_ingresos: float
    total_gastos: float
    balance: float
    gastos_por_categoria: List[GastoCategoria]

    class Config:
        from_attributes = True