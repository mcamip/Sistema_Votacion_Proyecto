from database import SessionLocal
from models import CarreraModel

# Abrimos una sesión de conexión
session = SessionLocal()

try:
    # Intentamos consultar las carreras registradas en Workbench
    carreras = session.query(CarreraModel).all()
    print("¡Conexión ORM exitosa! Total de carreras encontradas:", len(carreras))
except Exception as e:
    print("Ocurrió un error al conectar con la base de datos:", e)
finally:
    session.close()
    