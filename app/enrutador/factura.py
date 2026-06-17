from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.conexion_bd import get_session
from app.modelos import Factura, Transaccion

router = APIRouter(tags=["Factura"])

# === ENDPOINTS DE FACTURA ===
@router.get("/factura", summary="Listar Factura")
def listar_facturas(session: Session = Depends(get_session)):
    return session.exec(select(Factura)).all()

@router.post("/factura", summary="Crear Factura")
def crear_factura(factura: Factura, session: Session = Depends(get_session)):
    session.add(factura)
    session.commit()
    session.refresh(factura)
    return factura

@router.get("/factura/{id}", summary="Listar Factura Id")
def listar_factura_id(id: int, session: Session = Depends(get_session)):
    factura = session.get(Factura, id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    return factura

@router.put("/factura/{id}", summary="Editar Factura")
def editar_factura(id: int, factura_data: Factura, session: Session = Depends(get_session)):
    factura_db = session.get(Factura, id)
    if not factura_db:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    factura_db.numero_factura = factura_data.numero_factura
    factura_db.total = factura_data.total
    session.add(factura_db)
    session.commit()
    session.refresh(factura_db)
    return factura_db

@router.delete("/factura/{id}", summary="Eliminar Factura")
def eliminar_factura(id: int, session: Session = Depends(get_session)):
    factura = session.get(Factura, id)
    if not factura:
        raise HTTPException(status_code=404, detail="Factura no encontrada")
    session.delete(factura)
    session.commit()
    return {"detail": "Factura eliminada"}


# === ENDPOINTS DE TRANSACCIONES ===
@router.get("/factura/{id}/transacciones", summary="Listar Transacciones", tags=["Transacciones"])
def listar_transacciones(id: int, session: Session = Depends(get_session)):
    return session.exec(select(Transaccion).where(Transaccion.factura_id == id)).all()

@router.post("/factura/{id}/transacciones", summary="Agregar Transaccion", tags=["Transacciones"])
def agregar_transaccion(id: int, transaccion: Transaccion, session: Session = Depends(get_session)):
    transaccion.factura_id = id
    session.add(transaccion)
    session.commit()
    session.refresh(transaccion)
    return transaccion

@router.get("/factura/{id}/transacciones/{transacciones_id}", summary="Listar Transacciones Id", tags=["Transacciones"])
def listar_transaccion_id(id: int, transacciones_id: int, session: Session = Depends(get_session)):
    transaccion = session.get(Transaccion, transacciones_id)
    if not transaccion or transaccion.factura_id != id:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return transaccion

@router.put("/factura/{id}/transacciones/{transacciones_id}", summary="Editar Transacciones", tags=["Transacciones"])
def editar_transaccion(id: int, transacciones_id: int, transaccion_data: Transaccion, session: Session = Depends(get_session)):
    transaccion_db = session.get(Transaccion, transacciones_id)
    if not transaccion_db or transaccion_db.factura_id != id:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    transaccion_db.metodo_pago = transaccion_data.metodo_pago
    transaccion_db.estado = transaccion_data.estado
    session.add(transaccion_db)
    session.commit()
    session.refresh(transaccion_db)
    return transaccion_db

@router.delete("/factura/{id}/transacciones/{transacciones_id}", summary="Eliminar Transacciones", tags=["Transacciones"])
def eliminar_transaccion(id: int, transacciones_id: int, session: Session = Depends(get_session)):
    transaccion = session.get(Transaccion, transacciones_id)
    if not transaccion or transaccion.factura_id != id:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    session.delete(transaccion)
    session.commit()
    return {"detail": "Transacción eliminada"}