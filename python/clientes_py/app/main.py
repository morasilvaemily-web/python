from datetime import datetime

from fastapi import FastAPI, HTTPException
from modelos.clientes import Cliente, ClienteCrear, ClienteEditar
from modelos.facturas import Factura, FacturaCrear

app = FastAPI()

app = FastAPI()


app = FastAPI()


lista_clientes: list[Cliente] = []
lista_facturas: list[Factura] = []


@app.get("/clientes")
async def listar_clientes():
    # Creacion de sms mas adecuado al usuario
    return {"Clientes": lista_clientes}


@app.get("/clientes/{id}")
async def listar_cliente(id: int):
    
    for cliente in lista_clientes:
        if cliente.id == id:
            return cliente


@app.post("/clientes", response_model=Cliente)
async def crear_clientes(datos_cliente: ClienteCrear):
    cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    cliente_val.id = len(lista_clientes) + 1  # id incremento
    lista_clientes.append(cliente_val)
    return cliente_val
    

@app.put("/clientes/{id}")
def editar_clientes(id: int, datos_cliente: ClienteEditar):
    for i, obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id == id:
            cliente_val = Cliente.model_validate(datos_cliente.model_dump())
            cliente_val.id = id
            lista_clientes[i] = cliente_val

    return {
        "mensaje": "Se actualizo el cliente satisfactoriamente.",
        "Cliente": cliente_val,
    }


@app.delete("/clientes")
def eliminar_clientes():
    return {"Cliente": "Cliente eliminado"}





@app.get("/facturas", response_model=list[Factura])
async def listar_facturas():
    return lista_facturas


@app.post("/facturas/{cliente_id}", response_model=Factura)
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
            
            transaccion_val = Transacciones.model_validate(
                datos_transaccion.model_dump()
            )
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
