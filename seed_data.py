from database import SessionLocal, engine
import models
from datetime import datetime, timedelta
import random
import os

# Eliminar la base de datos existente si existe
if os.path.exists("isis_mobile.db"):
    os.remove("isis_mobile.db")

# Crear todas las tablas
models.Base.metadata.create_all(bind=engine)

# Crear una sesión
db = SessionLocal()

# Datos de ejemplo para celulares
celulares_data = [
    {
        "marca": "Samsung",
        "modelo": "Galaxy S23 Ultra",
        "precio": 1299.99,
        "stock": 15,
        "pantalla": "6.8 pulgadas AMOLED",
        "procesador": "Snapdragon 8 Gen 2",
        "ram": "12GB",
        "almacenamiento": "512GB",
        "camara": "200MP + 12MP + 10MP + 10MP"
    },
    {
        "marca": "iPhone",
        "modelo": "14 Pro Max",
        "precio": 1399.99,
        "stock": 10,
        "pantalla": "6.7 pulgadas Super Retina XDR",
        "procesador": "A16 Bionic",
        "ram": "6GB",
        "almacenamiento": "256GB",
        "camara": "48MP + 12MP + 12MP"
    },
    {
        "marca": "Xiaomi",
        "modelo": "13 Pro",
        "precio": 899.99,
        "stock": 20,
        "pantalla": "6.73 pulgadas AMOLED",
        "procesador": "Snapdragon 8 Gen 2",
        "ram": "12GB",
        "almacenamiento": "256GB",
        "camara": "50MP + 50MP + 50MP"
    }
]

# Datos de ejemplo para clientes
clientes_data = [
    {
        "nombre": "Juan",
        "apellido": "Pérez",
        "dni": "12345678",
        "email": "juan.perez@email.com",
        "telefono": "555-0101",
        "direccion": "Av. Principal 123",
        "historial_crediticio": 0.85
    },
    {
        "nombre": "María",
        "apellido": "González",
        "dni": "87654321",
        "email": "maria.gonzalez@email.com",
        "telefono": "555-0202",
        "direccion": "Calle Secundaria 456",
        "historial_crediticio": 0.92
    },
    {
        "nombre": "Carlos",
        "apellido": "Rodríguez",
        "dni": "23456789",
        "email": "carlos.rodriguez@email.com",
        "telefono": "555-0303",
        "direccion": "Plaza Central 789",
        "historial_crediticio": 0.78
    }
]

# Insertar celulares
celulares = []
for celular_data in celulares_data:
    celular = models.Celular(**celular_data)
    db.add(celular)
    celulares.append(celular)

# Insertar clientes
clientes = []
for cliente_data in clientes_data:
    cliente = models.Cliente(**cliente_data)
    db.add(cliente)
    clientes.append(cliente)

# Commit para obtener los IDs
db.commit()

# Crear solicitudes de crédito
solicitudes_data = []
for cliente in clientes:
    for _ in range(random.randint(1, 2)):  # 1-2 solicitudes por cliente
        celular = random.choice(celulares)
        solicitud = models.Solicitud(
            cliente_id=cliente.id,
            celular_id=celular.id,
            plazo_meses=random.choice([12, 18, 24]),
            ingreso_mensual=random.uniform(1000, 5000),
            estado='aprobado',
            documentos_respaldo=["solicitud_pendiente.pdf"],
            fecha_solicitud=datetime.now() - timedelta(days=random.randint(1, 30))
        )
        db.add(solicitud)
        solicitudes_data.append(solicitud)

db.commit()

# Crear pagos para las solicitudes aprobadas
for solicitud in solicitudes_data:
    cuota_mensual = solicitud.celular.precio / solicitud.plazo_meses
    pagos_realizados = random.randint(1, solicitud.plazo_meses)
    
    for mes in range(1, pagos_realizados + 1):
        pago = models.Pago(
            solicitud_id=solicitud.id,
            monto=cuota_mensual,
            fecha_pago=solicitud.fecha_solicitud + timedelta(days=30 * mes),
            numero_cuota=mes,
            cuotas_restantes=solicitud.plazo_meses - mes,
            estado="pagado"
        )
        db.add(pago)

# Commit final
db.commit()
db.close()

print("Base de datos poblada exitosamente con datos de prueba")

# Mostrar algunos datos de prueba
print("\nCelulares registrados:")
for celular in db.query(models.Celular).all():
    print(f"ID: {celular.id}, Marca: {celular.marca}, Modelo: {celular.modelo}")

print("\nClientes registrados:")
for cliente in db.query(models.Cliente).all():
    print(f"ID: {cliente.id}, Nombre: {cliente.nombre} {cliente.apellido}")

print("\nSolicitudes registradas:")
for solicitud in db.query(models.Solicitud).all():
    print(f"ID: {solicitud.id}, Cliente ID: {solicitud.cliente_id}, Estado: {solicitud.estado}")

print("\nPagos registrados:")
for pago in db.query(models.Pago).all():
    print(f"ID: {pago.id}, Solicitud ID: {pago.solicitud_id}, Monto: {pago.monto:.2f}")

db.close() 