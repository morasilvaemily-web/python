from fastapi import FastAPI
from modelos.clientes import Cliente, ClienteCrear, ClienteEditar


app = FastAPI()

#lista base de BD
lista_clientes:list[Cliente] = []
@app.get("/clientes")
async def listar_clientes():
    return{"clientes":lista_clientes}
@app.get("/clientes/{id}")
async def listar_clientes(id:int):
    #
    for cliente in lista_clientes:
        if cliente.id==id:
            return cliente 
@app.post("/clientes", response_model=Cliente)
async def crear_clientes(datos_cliente:ClienteCrear):
    cliente_val=Cliente.model_validate(datos_cliente.model_dump())
    cliente_val.id=len(lista_clientes)+1
    lista_clientes.append(cliente_val)
    return cliente_val
@app.put("/clientes/{id}")
def editar_clientes(id:int, datos_cliente:ClienteEditar):
    for i,obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id ==id:
            cliente_val=Cliente.model_validate(datos_cliente.model_dump())
            cliente_val.id =id
            lista_clientes[i] = cliente_val 
            return{"mensaje":"cliente editado.","Cliente":cliente_val}
@app.delete("/clientes/{id}")
def eliminar_clientes(id:int):
    for i,obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id == id:
            lista_clientes.pop(i)
            return{"mensaje":"cliente eliminado.","cliente":obj_cliente}
            
