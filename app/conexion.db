from sqlmodel import SQLModel, Session, create_engine
from typing import Annotated
from fastapi import Depends

nombre_bd = "bd_clientes_3407186.sqlite3"


url_bd = f"sqlite:///{nombre_bd}"


motor_db = create_engine(url_bd)



def obtener_sesion():
    with Session(motor_db) as mi_sesion:
        yield mi_sesion


Sesion_dependencia = Annotated(Session, Depends(obtener_sesion))
