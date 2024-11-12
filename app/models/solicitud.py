from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime
from enum import Enum

class EstadoCredito(str, Enum):
    PENDIENTE = "pendiente"
    APROBADO = "aprobado"
    RECHAZADO = "rechazado"
    EN_REVISION = "en_revision"

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