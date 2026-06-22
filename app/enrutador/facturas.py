from fastapi import APIRouter, HTTPException
from app.listas import listas_facturas, listas_clientes
from app.modelos.factura import *


router = APIRouter(
    prefix="/facturas",
    tags=["Facturas"]
)


# ===================================
# CRUD FACTURAS
# ===================================

@router.get("/", response_model=list[Factura])
async def listar_facturas():

    return listas_facturas


@router.get("/{id}")
async def obtener_factura(id: int):

    for factura in listas_facturas:

        if factura.id == id:
            return factura

    return {"error": "Factura no encontrada"}


@router.post("/{cliente_id}")
async def crear_factura(
    cliente_id: int,
    datos_factura: CrearFactura
):

    cliente_encontrado = None

    for cliente in listas_clientes:

        if cliente.id == cliente_id:
            cliente_encontrado = cliente
            break

    if not cliente_encontrado:

        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    factura_val = Factura.model_validate(
        datos_factura.model_dump()
    )

    factura_val.id = len(listas_facturas) + 1
    factura_val.cliente = cliente_encontrado

    listas_facturas.append(factura_val)

    return factura_val


@router.put("/{id}")
async def editar_factura(
    id: int,
    datos_factura: EditarFactura
):

    for i, factura in enumerate(listas_facturas):

        if factura.id == id:

            factura_val = Factura.model_validate(
                datos_factura.model_dump()
            )

            factura_val.id = id

            listas_facturas[i] = factura_val

            return {
                "mensaje": "Factura actualizada",
                "factura": factura_val
            }

    return {"error": "Factura no encontrada"}


@router.delete("/{id}")
async def eliminar_factura(id: int):

    for i, factura in enumerate(listas_facturas):

        if factura.id == id:

            del listas_facturas[i]

            return {
                "mensaje": "Factura eliminada"
            }

    return {"error": "Factura no encontrada"}