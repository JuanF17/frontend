from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Importaciones locales
from app.db.base import engine, Base, get_db
from app.core.config import settings
from app.models.celular import Celular
from app.models.cliente import Cliente
from app.models.solicitud import Solicitud
from app.schemas.cliente import ClienteCreate, ClienteResponse

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos y configurar templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Incluir las rutas de la API
from app.api.routes import api_router
app.include_router(api_router)

# Rutas de la interfaz web
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/admin")
async def admin_panel(request: Request, db: Session = Depends(get_db)):
    try:
        # Obtener datos con manejo de errores
        try:
            celulares = db.query(Celular).all()
            print(f"Celulares encontrados: {len(celulares)}")
        except Exception as e:
            print(f"Error al obtener celulares: {e}")
            celulares = []

        try:
            clientes = db.query(Cliente).all()
            print(f"Clientes encontrados: {len(clientes)}")
        except Exception as e:
            print(f"Error al obtener clientes: {e}")
            clientes = []

        try:
            solicitudes = db.query(Solicitud)\
                .join(Cliente)\
                .join(Celular)\
                .order_by(Solicitud.fecha_solicitud.desc())\
                .all()
            print(f"Solicitudes encontradas: {len(solicitudes)}")
        except Exception as e:
            print(f"Error al obtener solicitudes: {e}")
            solicitudes = []

        return templates.TemplateResponse("admin.html", {
            "request": request,
            "celulares": celulares,
            "clientes": clientes,
            "solicitudes": solicitudes
        })
    except Exception as e:
        print(f"Error general en admin_panel: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/consulta-cliente")
async def consulta_cliente_page(request: Request):
    return templates.TemplateResponse("consulta_cliente.html", {"request": request})

@app.get("/registro-cliente")
async def registro_cliente_page(request: Request):
    return templates.TemplateResponse("registro_cliente.html", {"request": request})

@app.get("/crear-credito")
async def crear_credito_page(request: Request, db: Session = Depends(get_db)):
    celulares = db.query(Celular).filter(Celular.stock > 0).all()
    return templates.TemplateResponse("crear_credito.html", {
        "request": request,
        "celulares": celulares
    })

@app.get("/pagos")
async def pagos_page(request: Request):
    return templates.TemplateResponse("pagos.html", {"request": request})