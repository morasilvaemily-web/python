from pydantic import BaseModel
class factura(BaseModel):
    id: int
    fecha: date
    total: float
    cliente: str | None
