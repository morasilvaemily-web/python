from fastapi import APIRouter, HTTPException
from app.modelos.clientes import Cliente
from app.listas_app import lista_clientes

ruta_clientes = APIRouter()

# 1. Listar todos los clientes
@ruta_clientes.get("/", summary="Listar Clientes", response_model=list[Cliente])
async def listar_clientes():
    return lista_clientes

# 2. Crear un nuevo cliente
@ruta_clientes.post("/", summary="Crear Clientes", response_model=Cliente)
async def crear_cliente(cliente: Cliente):
    cliente.id = len(lista_clientes) + 1
    lista_clientes.append(cliente)
    return cliente

# 3. EDITAR CLIENTE (Usando PATCH como te lo pide el profe)
@ruta_clientes.patch("/{id}", summary="Editar Clientes", response_model=Cliente)
async def editar_cliente(id: int, cliente_data: Cliente):
    for c in lista_clientes:
        if c.id == id:
            c.nombre = cliente_data.nombre
            c.email = cliente_data.email
            return c
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

# 4. Listar un único cliente por su ID
@ruta_clientes.get("/{id}", summary="Listar Cliente", response_model=Cliente)
async def listar_cliente_id(id: int):
    for c in lista_clientes:
        if c.id == id:
            return c
    raise HTTPException(status_code=404, detail="Cliente no encontrado")

# 5. Eliminar un cliente
@ruta_clientes.delete("/{id}", summary="Eliminar Cliente")
async def eliminar_cliente(id: int):
    for idx, c in enumerate(lista_clientes):
        if c.id == id:
            lista_clientes.pop(idx)
            return {"detail": "Cliente eliminado con éxito"}
    raise HTTPException(status_code=404, detail="Cliente no encontrado")