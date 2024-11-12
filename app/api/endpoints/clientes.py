from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.services.cliente_service import ClienteService
from app.schemas.cliente import ClienteCreate, ClienteUpdate, ClienteResponse
from typing import List
from app.models.cliente import Cliente
from app.models.solicitud import Solicitud
from app.models.celular import Celular

router = APIRouter()

@router.get("/", response_model=List[ClienteResponse])
def get_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return ClienteService.get_clientes(db, skip=skip, limit=limit)

@router.post("/", response_model=ClienteResponse)
def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    return ClienteService.create_cliente(db, cliente)

@router.get("/{cliente_id}", response_model=ClienteResponse)
def get_cliente(cliente_id: int, db: Session = Depends(get_db)):
    return ClienteService.get_cliente(db, cliente_id)

@router.get("/buscar/{dni}", response_model=dict)
def get_cliente_by_dni(dni: str, db: Session = Depends(get_db)):
    try:
        # Buscar cliente por DNI
        cliente = db.query(Cliente).filter(Cliente.dni == dni).first()
        if not cliente:
            raise HTTPException(status_code=404, detail="Cliente no encontrado")

        # Buscar créditos activos del cliente
        creditos = db.query(Solicitud)\
            .filter(Solicitud.cliente_id == cliente.id)\
            .filter(Solicitud.estado == 'aprobado')\
            .join(Celular)\
            .all()

        # Preparar la respuesta
        return {
            "cliente": {
                "id": cliente.id,
                "nombre": cliente.nombre,
                "apellido": cliente.apellido,
                "dni": cliente.dni,
                "email": cliente.email,
                "telefono": cliente.telefono,
                "direccion": cliente.direccion
            },
            "creditos": [{
                "id": credito.id,
                "celular": {
                    "marca": credito.celular.marca,
                    "modelo": credito.celular.modelo
                },
                "monto": credito.celular.precio,
                "plazo_meses": credito.plazo_meses,
                "estado": credito.estado,
                "fecha_solicitud": credito.fecha_solicitud
            } for credito in creditos]
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Error al buscar cliente: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{cliente_id}", response_model=ClienteResponse)
def update_cliente(cliente_id: int, cliente: ClienteUpdate, db: Session = Depends(get_db)):
    return ClienteService.update_cliente(db, cliente_id, cliente)

@router.delete("/{cliente_id}")
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    ClienteService.delete_cliente(db, cliente_id)
    return {"message": "Cliente eliminado correctamente"} 