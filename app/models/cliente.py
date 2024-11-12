from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.db.base import Base

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