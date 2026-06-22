from fastapi import APIRouter, HTTPException
from app.listas import listas_transacciones, listas_facturas
from app.model.transacciones import *

router = APIRouter(
    prefix="/transacciones",
    tags=["Transacciones"]
)

# ===================================
# CRUD TRANSACCIONES
# ===================================

@router.get("/transacciones")
async def listar_transacciones():

    return listas_transacciones


@router.get("/transacciones/{id}")
async def obtener_transaccion(id: int):

    for transaccion in listas_transacciones:

        if transaccion.id == id:
            return transaccion

    return {"error": "Transacción no encontrada"}


@router.post("/transacciones/{factura_id}")
async def crear_transaccion(
    factura_id: int,
    datos_transaccion: TransaccionCrear
):

    factura_encontrada = None

    for factura in listas_facturas:

        if factura.id == factura_id:
            factura_encontrada = factura
            break

    if not factura_encontrada:

        raise HTTPException(
            status_code=404,
            detail="Factura no encontrada"
        )

    transaccion_val = Transaccion.model_validate(
        datos_transaccion.model_dump()
    )

    transaccion_val.id = len(listas_transacciones) + 1
    transaccion_val.factura_id = factura_id

    listas_transacciones.append(transaccion_val)

    factura_encontrada.transacciones.append(
        transaccion_val
    )

    return {
        "mensaje": "Transacción creada",
        "transaccion": transaccion_val
    }


@router.put("/transacciones/{id}")
async def editar_transaccion(
    id: int,
    datos_transaccion: TransaccionEditar
):

    for i, transaccion in enumerate(
        listas_transacciones
    ):

        if transaccion.id == id:

            transaccion_val = Transaccion.model_validate(
                datos_transaccion.model_dump()
            )

            transaccion_val.id = id
            transaccion_val.factura_id = (
                transaccion.factura_id
            )

            listas_transacciones[i] = transaccion_val

            return {
                "mensaje": "Transacción actualizada",
                "transaccion": transaccion_val
            }

    return {"error": "Transacción no encontrada"}


@router.delete("/transacciones/{id}")
async def eliminar_transaccion(id: int):

    for i, transaccion in enumerate(
        listas_transacciones
    ):

        if transaccion.id == id:

            del listas_transacciones[i]

            return {
                "mensaje": "Transacción eliminada"
            }

    return {"error": "Transacción no encontrada"}