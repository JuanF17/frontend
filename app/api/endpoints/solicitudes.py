from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.services.solicitud_service import SolicitudService
from app.schemas.solicitud import SolicitudCreate, SolicitudUpdate, SolicitudResponse
from typing import List

router = APIRouter()

@router.get("/", response_model=List[SolicitudResponse])
def get_solicitudes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return SolicitudService.get_solicitudes(db, skip=skip, limit=limit)

@router.post("/", response_model=SolicitudResponse)
def create_solicitud(solicitud: SolicitudCreate, db: Session = Depends(get_db)):
    return SolicitudService.create_solicitud(db, solicitud)

@router.get("/{solicitud_id}", response_model=SolicitudResponse)
def get_solicitud(solicitud_id: int, db: Session = Depends(get_db)):
    return SolicitudService.get_solicitud(db, solicitud_id)

@router.put("/{solicitud_id}", response_model=SolicitudResponse)
def update_solicitud(solicitud_id: int, solicitud: SolicitudUpdate, db: Session = Depends(get_db)):
    return SolicitudService.update_solicitud(db, solicitud_id, solicitud)

@router.put("/{solicitud_id}/estado")
def update_estado(solicitud_id: int, estado: str, db: Session = Depends(get_db)):
    return SolicitudService.update_estado(db, solicitud_id, estado)

@router.delete("/{solicitud_id}")
def delete_solicitud(solicitud_id: int, db: Session = Depends(get_db)):
    SolicitudService.delete_solicitud(db, solicitud_id)
    return {"message": "Solicitud eliminada correctamente"}

@router.get("/cliente/{cliente_id}", response_model=List[SolicitudResponse])
def get_solicitudes_by_cliente(cliente_id: int, db: Session = Depends(get_db)):
    return SolicitudService.get_solicitudes_by_cliente(db, cliente_id)

@router.get("/estado/{estado}", response_model=List[SolicitudResponse])
def get_solicitudes_by_estado(estado: str, db: Session = Depends(get_db)):
    return SolicitudService.get_solicitudes_by_estado(db, estado) 