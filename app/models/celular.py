from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.db.base import Base

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
    
    solicitudes = relationship("Solicitud", back_populates="celular") 