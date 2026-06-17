from pydantic import BaseModel


class Factura(BaseModel):
    id: int
    numero_factura: str
    cliente_id: int
    total: float
    estado: str


class FacturaCrear(BaseModel):
    numero_factura: str
    cliente_id: int
    total: float
    estado: str


class FacturaEditar(BaseModel):
    numero_factura: str
    cliente_id: int
    total: float
    estado: str