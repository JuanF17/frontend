from fastapi import APIRouter
from app.api.endpoints import celulares, clientes, solicitudes, pagos

api_router = APIRouter()

# Incluir los routers de cada endpoint con los prefijos correctos
api_router.include_router(
    celulares.router,
    prefix="/api/celulares",
    tags=["celulares"]
)

api_router.include_router(
    clientes.router,
    prefix="/api/clientes",
    tags=["clientes"]
)

api_router.include_router(
    solicitudes.router,
    prefix="/api/solicitudes",
    tags=["solicitudes"]
)

api_router.include_router(
    pagos.router,
    prefix="/api/pagos",
    tags=["pagos"]
) 