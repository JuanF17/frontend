from sqlalchemy.orm import Session
from app.models.solicitud import Solicitud, EstadoCredito
from app.schemas.solicitud import SolicitudCreate, SolicitudUpdate
from fastapi import HTTPException

class SolicitudService:
    @staticmethod
    def get_solicitudes(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Solicitud)\
            .join(Solicitud.cliente)\
            .join(Solicitud.celular)\
            .order_by(Solicitud.fecha_solicitud.desc())\
            .offset(skip)\
            .limit(limit)\
            .all()

    @staticmethod
    def get_solicitud(db: Session, solicitud_id: int):
        solicitud = db.query(Solicitud)\
            .filter(Solicitud.id == solicitud_id)\
            .first()
        if not solicitud:
            raise HTTPException(status_code=404, detail="Solicitud no encontrada")
        return solicitud

    @staticmethod
    def create_solicitud(db: Session, solicitud: SolicitudCreate):
        db_solicitud = Solicitud(
            cliente_id=solicitud.cliente_id,
            celular_id=solicitud.celular_id,
            plazo_meses=solicitud.plazo_meses,
            ingreso_mensual=solicitud.ingreso_mensual,
            estado=EstadoCredito.PENDIENTE,
            documentos_respaldo=solicitud.documentos_respaldo
        )
        db.add(db_solicitud)
        db.commit()
        db.refresh(db_solicitud)
        return db_solicitud

    @staticmethod
    def update_solicitud(db: Session, solicitud_id: int, solicitud: SolicitudUpdate):
        db_solicitud = SolicitudService.get_solicitud(db, solicitud_id)
        for key, value in solicitud.dict(exclude_unset=True).items():
            setattr(db_solicitud, key, value)
        db.commit()
        db.refresh(db_solicitud)
        return db_solicitud

    @staticmethod
    def delete_solicitud(db: Session, solicitud_id: int):
        solicitud = SolicitudService.get_solicitud(db, solicitud_id)
        db.delete(solicitud)
        db.commit()
        return solicitud

    @staticmethod
    def update_estado(db: Session, solicitud_id: int, nuevo_estado: str):
        solicitud = SolicitudService.get_solicitud(db, solicitud_id)
        if nuevo_estado not in [e.value for e in EstadoCredito]:
            raise HTTPException(status_code=400, detail="Estado no válido")
        solicitud.estado = nuevo_estado
        db.commit()
        db.refresh(solicitud)
        return solicitud

    @staticmethod
    def get_solicitudes_by_cliente(db: Session, cliente_id: int):
        return db.query(Solicitud)\
            .filter(Solicitud.cliente_id == cliente_id)\
            .order_by(Solicitud.fecha_solicitud.desc())\
            .all()

    @staticmethod
    def get_solicitudes_by_estado(db: Session, estado: str):
        if estado not in [e.value for e in EstadoCredito]:
            raise HTTPException(status_code=400, detail="Estado no válido")
        return db.query(Solicitud)\
            .filter(Solicitud.estado == estado)\
            .order_by(Solicitud.fecha_solicitud.desc())\
            .all() 