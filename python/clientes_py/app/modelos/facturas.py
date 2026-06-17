from pydantic import BaseModel, computed_field

from modelos.clientes import Cliente


class FacturaBase(BaseModel):
    fecha: str
    cliente: Cliente

    @computed_field
    @property
    def valor_total(self) -> float:
        
        factura_id_actual = getattr(self, "id", None)
        if factura_id_actual is None or not self.transacciones:
            return 0.0
        return sum(
            t.cantidad * t.vr_unitario
            for t in self.transacciones
            if t.factura_id == factura_id_actual
        )


class FacturaCrear(FacturaBase):
    pass


class FacturaEditar(FacturaBase):
    pass


class Factura(FacturaBase):
    id: int | None = None
