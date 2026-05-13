from pydantic import BaseModel

class ClientBase(BaseModel):
    nombre: str
    edad: int
    descripcion: str |None
    
class ClienteCrear(ClientBase):
        pass
class ClienteEditar(ClientBase):
        pass
class Cliente(ClientBase):
        id: int | None=None