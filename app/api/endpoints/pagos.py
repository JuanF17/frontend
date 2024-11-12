from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.pago import Pago
from app.models.solicitud import Solicitud
from app.models.cliente import Cliente
from datetime import datetime

router = APIRouter()

@router.get("/cliente/{dni}")
async def get_pagos_cliente(dni: str, db: Session = Depends(get_db)):
    # Buscar cliente por DNI
    cliente = db.query(Cliente).filter(Cliente.dni == dni).first()
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")

    # Buscar solicitudes aprobadas del cliente
    solicitudes = db.query(Solicitud)\
        .filter(Solicitud.cliente_id == cliente.id)\
        .filter(Solicitud.estado == 'aprobado')\
        .all()

    # Preparar respuesta con información de pagos
    creditos_info = []
    for solicitud in solicitudes:
        pagos_realizados = db.query(Pago)\
            .filter(Pago.solicitud_id == solicitud.id)\
            .order_by(Pago.fecha_pago)\
            .all()

        monto_total = solicitud.celular.precio
        cuota_mensual = monto_total / solicitud.plazo_meses
        cuotas_pagadas = len(pagos_realizados)
        cuotas_restantes = solicitud.plazo_meses - cuotas_pagadas

        creditos_info.append({
            "solicitud_id": solicitud.id,
            "celular": f"{solicitud.celular.marca} {solicitud.celular.modelo}",
            "monto_total": monto_total,
            "cuota_mensual": cuota_mensual,
            "plazo_total": solicitud.plazo_meses,
            "cuotas_pagadas": cuotas_pagadas,
            "cuotas_restantes": cuotas_restantes,
            "pagos": [{
                "id": pago.id,
                "monto": pago.monto,
                "fecha": pago.fecha_pago,
                "numero_cuota": pago.numero_cuota
            } for pago in pagos_realizados]
        })

    return {
        "cliente": {
            "nombre": f"{cliente.nombre} {cliente.apellido}",
            "dni": cliente.dni
        },
        "creditos": creditos_info
    }

@router.post("/realizar/{solicitud_id}")
async def realizar_pago(solicitud_id: int, db: Session = Depends(get_db)):
    # Verificar que la solicitud existe y está aprobada
    solicitud = db.query(Solicitud)\
        .filter(Solicitud.id == solicitud_id)\
        .filter(Solicitud.estado == 'aprobado')\
        .first()
    
    if not solicitud:
        raise HTTPException(status_code=404, detail="Solicitud no encontrada o no aprobada")

    # Calcular información del pago
    monto_total = solicitud.celular.precio
    cuota_mensual = monto_total / solicitud.plazo_meses
    
    # Contar pagos existentes
    pagos_realizados = db.query(Pago)\
        .filter(Pago.solicitud_id == solicitud_id)\
        .count()
    
    if pagos_realizados >= solicitud.plazo_meses:
        raise HTTPException(status_code=400, detail="Todas las cuotas ya están pagadas")

    # Crear nuevo pago
    nuevo_pago = Pago(
        solicitud_id=solicitud_id,
        monto=cuota_mensual,
        numero_cuota=pagos_realizados + 1,
        cuotas_restantes=solicitud.plazo_meses - (pagos_realizados + 1)
    )

    db.add(nuevo_pago)
    db.commit()
    db.refresh(nuevo_pago)

    return {
        "mensaje": "Pago realizado correctamente",
        "pago_id": nuevo_pago.id,
        "monto": nuevo_pago.monto,
        "cuota_numero": nuevo_pago.numero_cuota,
        "cuotas_restantes": nuevo_pago.cuotas_restantes
    } 