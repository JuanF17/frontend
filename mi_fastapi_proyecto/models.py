from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum

class EstadoCredito(str, Enum):
    PENDIENTE = "pendiente"
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"
    EN_REVISION = "en_revision"

class CelularBase(BaseModel):
    marca: str
    modelo: str
    precio: float
    stock: int
    especificaciones: dict

class SolicitudCredito(BaseModel):
    cliente_id: int
    celular_id: int
    plazo_meses: int
    ingreso_mensual: float
    documentos_respaldo: List[str]

class Cliente(BaseModel):
    nombre: str
    apellido: str
    dni: str
    email: str
    telefono: str
    direccion: str
    historial_crediticio: Optional[float] = None

class Pago(BaseModel):
    credito_id: int
    monto: float
    fecha_pago: datetime
    estado: str