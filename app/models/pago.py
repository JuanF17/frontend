from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from app.db.base import Base
from datetime import datetime

class Pago(Base):
    __tablename__ = "pagos"

    id = Column(Integer, primary_key=True, index=True)
    solicitud_id = Column(Integer, ForeignKey("solicitudes.id", ondelete="CASCADE"))
    monto = Column(Float)
    fecha_pago = Column(DateTime, default=datetime.utcnow)
    numero_cuota = Column(Integer)  # Número de cuota que se está pagando
    cuotas_restantes = Column(Integer)  # Cuotas que quedan por pagar
    estado = Column(String, default="pagado")  # pagado, pendiente, atrasado

    solicitud = relationship("Solicitud")  # Simplificamos la relación