from sqlmodel import SQLModel, Field, Relationship



class TransaccionBase(SQLModel):
    cantidad: int
    vr_unitario: float
    descripcion: str


class TransaccionCrear(SQLModel):
    cantidad: int
    vr_unitario: float
    descripcion: str


class TransaccionEditar(SQLModel):
    cantidad: int
    vr_unitario: float
    descripcion: str

class Transaccion(TransaccionBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    factura_id: int | None = Field(
        default=None,
        foreign_key="factura.id"
    )