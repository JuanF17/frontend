from pydantic import BaseModel
from typing import List
from datetime import datetime
from ..models.solicitud import EstadoCredito

class SolicitudBase(BaseModel):
    cliente_id: int
    celular_id: int
    plazo_meses: int
    ingreso_mensual: float
    estado: str = 'pendiente'
    documentos_respaldo: List[str] = ["solicitud_pendiente.pdf"]

class SolicitudCreate(SolicitudBase):
    pass

class SolicitudUpdate(SolicitudBase):
    pass

class SolicitudResponse(SolicitudBase):
    id: int
    estado: EstadoCredito
    fecha_solicitud: datetime

    class Config:
        from_attributes = True 