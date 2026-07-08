from fastapi import APIRouter, HTTPException
from app.modelos.facturas import Factura, CrearFactura, EditarFactura
from app.modelos.clientes import Cliente
from ..conexion_bd import Sesion_dependencia
from sqlmodel import select

router = APIRouter(
    prefix="/facturas",
    tags=["Facturas"]
)


# ===================================
# CRUD FACTURAS
# ===================================
@router.get("/", response_model=list[Factura])
async def listar_facturas(mi_sesion: Sesion_dependencia):

    facturas = mi_sesion.exec(select(Factura)).all()
    return facturas

@router.get("/{id}")
async def obtener_factura(
    id: int,
    mi_sesion: Sesion_dependencia
):

    factura = mi_sesion.get(Factura, id)

    if not factura:
        raise HTTPException(
            status_code=404,
            detail="Factura no encontrada"
        )

    return factura

@router.post("/{cliente_id}")
async def crear_factura(
    cliente_id: int,
    datos_factura: CrearFactura,
    mi_sesion: Sesion_dependencia
):

    cliente_encontrado = mi_sesion.get(Cliente, cliente_id)

    if not cliente_encontrado:
        raise HTTPException(
            status_code=404,
            detail="Cliente no encontrado"
        )

    factura_val = Factura.model_validate(datos_factura.model_dump())
    
    factura_val.cliente_id = cliente_id

    mi_sesion.add(factura_val)
    mi_sesion.commit()
    mi_sesion.refresh(factura_val)

    return factura_val


@router.put("/{id}")
async def editar_factura(
    id: int,
    datos_factura: EditarFactura,
    mi_sesion: Sesion_dependencia
):

    factura = mi_sesion.get(Factura, id)

    if not factura:
        raise HTTPException(
            status_code=404,
            detail="Factura no encontrada"
        )

    datos = datos_factura.model_dump(exclude_unset=True)

    factura.sqlmodel_update(datos)

    mi_sesion.add(factura)
    mi_sesion.commit()
    mi_sesion.refresh(factura)

    return factura

@router.put("/{id}")
async def editar_factura(
    id: int,
    datos_factura: EditarFactura,
    mi_sesion: Sesion_dependencia
):

    factura = mi_sesion.get(Factura, id)

    if not factura:
        raise HTTPException(
            status_code=404,
            detail="Factura no encontrada"
        )

    datos = datos_factura.model_dump(exclude_unset=True)

    factura.sqlmodel_update(datos)

    mi_sesion.add(factura)
    mi_sesion.commit()
    mi_sesion.refresh(factura)

    return factura

@router.delete("/{id}")
async def eliminar_factura(
    id: int,
    mi_sesion: Sesion_dependencia
):

    factura = mi_sesion.get(Factura, id)

    if not factura:
        raise HTTPException(
            status_code=404,
            detail="Factura no encontrada"
        )

    mi_sesion.delete(factura)
    mi_sesion.commit()

    return factura