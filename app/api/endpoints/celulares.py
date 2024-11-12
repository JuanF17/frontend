from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.services.celular_service import CelularService
from app.schemas.celular import CelularCreate, CelularUpdate, CelularResponse
from typing import List

router = APIRouter()

@router.get("/", response_model=List[CelularResponse])
def get_celulares(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return CelularService.get_celulares(db, skip=skip, limit=limit)

@router.post("/", response_model=CelularResponse)
def create_celular(celular: CelularCreate, db: Session = Depends(get_db)):
    return CelularService.create_celular(db, celular)

@router.get("/{celular_id}", response_model=CelularResponse)
def get_celular(celular_id: int, db: Session = Depends(get_db)):
    return CelularService.get_celular(db, celular_id)

@router.put("/{celular_id}", response_model=CelularResponse)
def update_celular(celular_id: int, celular: CelularUpdate, db: Session = Depends(get_db)):
    return CelularService.update_celular(db, celular_id, celular)

@router.delete("/{celular_id}")
def delete_celular(celular_id: int, db: Session = Depends(get_db)):
    CelularService.delete_celular(db, celular_id)
    return {"message": "Celular eliminado correctamente"} 