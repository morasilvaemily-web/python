from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

from app.modelos.clientes import Cliente


class FacturaBase(SQLModel):
    fecha: datetime


class CrearFactura(SQLModel):
    fecha: datetime


class EditarFactura(SQLModel):
    fecha: datetime

class Factura(FacturaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    cliente_id: int | None = Field(
        default=None,
        foreign_key="cliente.id"
    )