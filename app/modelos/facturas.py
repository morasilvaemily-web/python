from datetime import datetime
from sqlmodel import SQLModel, Field

from app.modelos.clientes import Cliente
from app.modelos.transacciones import Transaccion


class FacturaBase(SQLModel):
    fecha: datetime


class CrearFactura(SQLModel):
    fecha: datetime


class EditarFactura(SQLModel):
    fecha: datetime


class Factura(FacturaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)