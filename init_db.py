from database import create_tables
import seed_data

if __name__ == "__main__":
    print("Creando tablas...")
    create_tables()
    print("Tablas creadas exitosamente")
    
    print("Ejecutando script de datos de prueba...")
    # En lugar de llamar a populate_db(), ejecutamos el script directamente
    exec(open("seed_data.py").read())
    print("Base de datos poblada exitosamente") 