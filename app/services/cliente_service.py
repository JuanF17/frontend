from sqlalchemy.orm import Session
from app.models.cliente import Cliente
from app.schemas.cliente import ClienteCreate, ClienteUpdate
from fastapi import HTTPException

class ClienteService:
    @staticmethod
    def get_clientes(db: Session, skip: int = 0, limit: int = 100):
        return db.query(Cliente).offset(skip).limit(limit).all()

    @staticmethod
    def get_cliente(db: Session, cliente_id: int):
        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return cliente

    @staticmethod
    def get_cliente_by_dni(db: Session, dni: str):
        cliente = db.query(Cliente).filter(Cliente.dni == dni).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")
        return cliente

    @staticmethod
    def create_cliente(db: Session, cliente: ClienteCreate):
        # Verificar si ya existe un cliente con el mismo DNI
        if db.query(Cliente).filter(Cliente.dni == cliente.dni).first():
            raise HTTPException(status_code=400, detail="Ya existe un cliente con este DNI")
        
        # Verificar si ya existe un cliente con el mismo email
        if db.query(Cliente).filter(Cliente.email == cliente.email).first():
            raise HTTPException(status_code=400, detail="Ya existe un cliente con este email")

        db_cliente = Cliente(**cliente.dict())
        db.add(db_cliente)
        db.commit()
        db.refresh(db_cliente)
        return db_cliente

    @staticmethod
    def update_cliente(db: Session, cliente_id: int, cliente: ClienteUpdate):
        db_cliente = ClienteService.get_cliente(db, cliente_id)
        for key, value in cliente.dict().items():
            setattr(db_cliente, key, value)
        db.commit()
        db.refresh(db_cliente)
        return db_cliente

    @staticmethod
    def delete_cliente(db: Session, cliente_id: int):
        cliente = ClienteService.get_cliente(db, cliente_id)
        db.delete(cliente)
        db.commit()
        return cliente 