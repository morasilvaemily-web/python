from pydantic import BaseModel
from typing import Optional

# Este modelo sirve para cuando el usuario envía datos desde Swagger/Frontend
class TransaccionesCrear(BaseModel):
    metodo_pago: str  # Ejemplo: "Efectivo" o "Tarjeta"
    estado: str       # Ejemplo: "Exitoso" o "Pendiente"
    cantidad: int
    vr_unitario: float

# Este modelo representa la transacción completa ya guardada con sus IDs generados
class Transacciones(BaseModel):
    id: Optional[int] = None
    factura_id: Optional[int] = None
    metodo_pago: str
    estado: str
    cantidad: int
    vr_unitario: float