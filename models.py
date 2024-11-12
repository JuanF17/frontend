from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime
from enum import Enum

# Enums
class EstadoCredito(str, Enum):
    PENDIENTE = "pendiente"
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"
    EN_REVISION = "en_revision"

# Modelos SQLAlchemy
class Celular(Base):
    __tablename__ = "celulares"

    id = Column(Integer, primary_key=True, index=True)
    marca = Column(String, nullable=False)
    modelo = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    stock = Column(Integer, nullable=False)
    pantalla = Column(String, nullable=False)
    procesador = Column(String, nullable=False)
    ram = Column(String, nullable=False)
    almacenamiento = Column(String, nullable=False)
    camara = Column(String, nullable=False)
    
    # Agregar relación con solicitudes
    solicitudes = relationship("Solicitud", back_populates="celular")

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    apellido = Column(String)
    dni = Column(String, unique=True, index=True)
    email = Column(String, unique=True)
    telefono = Column(String)
    direccion = Column(String)
    historial_crediticio = Column(Float, nullable=True)
    
    solicitudes = relationship("Solicitud", back_populates="cliente", cascade="all, delete-orphan")

class Solicitud(Base):
    __tablename__ = "solicitudes"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id", ondelete="CASCADE"))
    celular_id = Column(Integer, ForeignKey("celulares.id", ondelete="CASCADE"))
    plazo_meses = Column(Integer)
    ingreso_mensual = Column(Float)
    documentos_respaldo = Column(JSON)
    estado = Column(SQLEnum(EstadoCredito), default=EstadoCredito.PENDIENTE)
    fecha_solicitud = Column(DateTime, default=datetime.utcnow)

    cliente = relationship("Cliente", back_populates="solicitudes")
    celular = relationship("Celular", back_populates="solicitudes")
    pagos = relationship("Pago", back_populates="solicitud", cascade="all, delete-orphan")

class Pago(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    solicitud_id = Column(Integer, ForeignKey("solicitudes.id", ondelete="CASCADE"))
    monto = Column(Float)
    fecha_pago = Column(DateTime, default=datetime.utcnow)
    estado = Column(String)

    solicitud = relationship("Solicitud", back_populates="pagos")

# Esquemas Pydantic
from pydantic import BaseModel
from typing import Optional, List

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

class ClienteResponse(ClienteBase):
    id: int

    class Config:
        from_attributes = True

class SolicitudBase(BaseModel):
    cliente_id: int
    celular_id: int
    plazo_meses: int
    ingreso_mensual: float
    estado: str = 'pendiente'
    documentos_respaldo: List[str] = ["solicitud_pendiente.pdf"]

class SolicitudCreate(SolicitudBase):
    pass

class SolicitudResponse(SolicitudBase):
    id: int
    estado: EstadoCredito
    fecha_solicitud: datetime

    class Config:
        from_attributes = True

class PagoBase(BaseModel):
    solicitud_id: int
    monto: float
    estado: str

class PagoCreate(PagoBase):
    pass

class PagoResponse(PagoBase):
    id: int
    fecha_pago: datetime

    class Config:
        from_attributes = True