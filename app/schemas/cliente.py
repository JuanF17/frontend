from pydantic import BaseModel
from typing import Optional

class ClienteBase(BaseModel):
    nombre: str
    apellido: str
    dni: str
    email: str
    telefono: str
    direccion: str
    historial_crediticio: Optional[float] = None

class ClienteCreate(ClienteBase):
    pass

class ClienteUpdate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: int

    class Config:
        from_attributes = True 