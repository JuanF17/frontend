from pydantic import BaseModel

class CelularBase(BaseModel):
    marca: str
    modelo: str
    precio: float
    stock: int
    pantalla: str
    procesador: str
    ram: str
    almacenamiento: str
    camara: str

class CelularCreate(CelularBase):
    pass

class CelularUpdate(CelularBase):
    pass

class CelularResponse(CelularBase):
    id: int

    class Config:
        from_attributes = True 