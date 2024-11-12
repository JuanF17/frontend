from sqlalchemy.orm import Session
from app.models.celular import Celular
from app.schemas.celular import CelularCreate, CelularUpdate
from fastapi import HTTPException

class CelularService:
    @staticmethod
    def get_celulares(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Celular).offset(skip).limit(limit).all()

    @staticmethod
    def get_celular(db: Session, celular_id: int):
        celular = db.query(Celular).filter(Celular.id == celular_id).first()
        if not celular:
            raise HTTPException(status_code=404, detail="Celular no encontrado")
        return celular

    @staticmethod
    def create_celular(db: Session, celular: CelularCreate):
        db_celular = Celular(**celular.dict())
        db.add(db_celular)
        db.commit()
        db.refresh(db_celular)
        return db_celular

    @staticmethod
    def update_celular(db: Session, celular_id: int, celular: CelularUpdate):
        db_celular = CelularService.get_celular(db, celular_id)
        for key, value in celular.dict().items():
            setattr(db_celular, key, value)
        db.commit()
        db.refresh(db_celular)
        return db_celular

    @staticmethod
    def delete_celular(db: Session, celular_id: int):
        celular = CelularService.get_celular(db, celular_id)
        db.delete(celular)
        db.commit()
        return celular 