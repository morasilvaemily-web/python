from datetime import datetime
from fastapi import FastAPI, HTTPException
from app.modelos.clientes import Cliente, ClienteCrear, ClienteEditar
from app.modelos.facturas import Factura, FacturaCrear
from app.modelos.transacciones import Transacciones, TransaccionesCrear
from app.enrutador import clientes
from app.listas_app import lista_clientes, lista_facturas, lista_transacciones

app = FastAPI()

# 1. Tus 5 rutas de clientes (Las jala de tu enrutador)
app.include_router(clientes.ruta_clientes, tags=["Clientes"])


# ==========================================
#   2. ENDPOINT DE FACTURAS (Tus 5 rutas)
# ==========================================

@app.get("/facturas", response_model=list[Factura], tags=["Factura"])
async def listar_facturas():
    return lista_facturas

@app.post("/facturas/{cliente_id}", response_model=Factura, tags=["Factura"])
async def crear_facturas(cliente_id: int, datos_factura: FacturaCrear):
    cliente_encontrado = None
    for c in lista_clientes:
        if c.id == cliente_id:
            cliente_encontrado = c
            break

    if not cliente_encontrado:
        raise HTTPException(
            status_code=400,
            detail=f"Cliente con id {cliente_id} no existe, debes crear.",
        )

    factura_val = Factura.model_validate(datos_factura.model_dump())
    factura_val.id = len(lista_facturas) + 1
    factura_val.fecha = datetime.now()
    factura_val.cliente = cliente_encontrado
    lista_facturas.append(factura_val)
    return factura_val

@app.get("/facturas/{id}", response_model=Factura, tags=["Factura"])
async def listar_factura_id(id: int):
    for f in lista_facturas:
        if f.id == id:
            return f
    raise HTTPException(status_code=404, detail="Factura no encontrada")

@app.put("/facturas/{id}", response_model=Factura, tags=["Factura"])
async def editar_factura(id: int, datos_factura: FacturaCrear):
    for f in lista_facturas:
        if f.id == id:
            f.total = datos_factura.total
            return f
    raise HTTPException(status_code=404, detail="Factura no encontrada")

@app.delete("/facturas/{id}", tags=["Factura"])
async def eliminar_factura(id: int):
    for idx, f in enumerate(lista_facturas):
        if f.id == id:
            lista_facturas.pop(idx)
            return {"detail": "Factura de cliente eliminada"}
    raise HTTPException(status_code=404, detail="Factura no encontrada")


# ==========================================
#   3. ENDPOINT DE TRANSACCIONES (Tus 5 rutas)
# ==========================================

@app.get("/transacciones", response_model=list[Transacciones], tags=["Transacciones"])
async def listar_transacciones():
    return lista_transacciones

@app.post("/transacciones/{factura_id}", tags=["Transacciones"])
async def crear_transaccion(factura_id: int, datos_transaccion: TransaccionesCrear, cliente_id: int):
    cliente_encontrado = None
    for c in lista_clientes:
        if c.id == cliente_id:
            cliente_encontrado = c
            break

    if not cliente_encontrado:
        raise HTTPException(
            status_code=400,
            detail=f"Error 400: No existe un cliente con ese id: {cliente_id}, debes crear el cliente.",
        )

    factura_encontrada = None
    for f in lista_facturas:
        if f.id == factura_id:
            factura_encontrada = f
            break

    if factura_encontrada:
        if factura_encontrada.cliente.id == cliente_id:
            transaccion_val = Transacciones.model_validate(datos_transaccion.model_dump())
            transaccion_val.id = len(lista_transacciones) + 1
            transaccion_val.factura_id = factura_id
            lista_transacciones.append(transaccion_val)

            factura_encontrada.transacciones.append(transaccion_val)
            mensaje = f"Transaccion agregada a factura {factura_encontrada.id}"
            factura_final = factura_encontrada
            return {"mensaje": mensaje, "factura": factura_final}
        else:
            mensaje = f"Se encontro la factura de id: {factura_id}, pero es de otro cliente id: {cliente_id}"
            factura_final = factura_encontrada
            return {"mensaje": mensaje, "factura encontrada": factura_final}
    else:
        transaccion_val = Transacciones.model_validate(datos_transaccion.model_dump())
        transaccion_val.id = len(lista_transacciones) + 1
        transaccion_val.factura_id = len(lista_facturas) + 1

        factura = FacturaCrear(
            cliente=cliente_encontrado,
            fecha=str(datetime.now()),
            transacciones=[transaccion_val],
        )

        factura_val = Factura.model_validate(factura.model_dump())
        factura_val.id = len(lista_facturas) + 1
        lista_facturas.append(factura_val)
        lista_transacciones.append(transaccion_val)

        return {
            "mensaje": f"Factura no existe con el id: {factura_id}, pero se creo la nueva factura",
            "facturas": transaccion_val,
        }

@app.get("/transacciones/{id}", response_model=Transacciones, tags=["Transacciones"])
async def listar_transaccion_id(id: int):
    for t in lista_transacciones:
        if t.id == id:
            return t
    raise HTTPException(status_code=404, detail="Transacción no encontrada")

@app.put("/transacciones/{id}", response_model=Transacciones, tags=["Transacciones"])
async def editar_transaccion(id: int, datos_transaccion: TransaccionesCrear):
    for t in lista_transacciones:
        if t.id == id:
            t.metodo_pago = datos_transaccion.metodo_pago
            t.estado = datos_transaccion.estado
            return t
    raise HTTPException(status_code=404, detail="Transacción no encontrada")

@app.delete("/transacciones/{id}", tags=["Transacciones"])
async def eliminar_transaccion(id: int):
    for idx, t in enumerate(lista_transacciones):
        if t.id == id:
            lista_transacciones.pop(idx)
            return {"detail": "Transacción eliminada con éxito"}
    raise HTTPException(status_code=404, detail="Transacción no encontrada")