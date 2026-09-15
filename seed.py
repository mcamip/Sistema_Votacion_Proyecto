from database import SessionLocal
from models import CarreraModel, EstudianteModel

def seed_database():
    session = SessionLocal()
    try:
        # Verificamos si ya existen carreras para no duplicarlas
        carreras_existentes = session.query(CarreraModel).count()
        if carreras_existentes > 0:
            print("¡La base de datos ya tiene registros! No es necesario insertar de nuevo.")
            return

        print("Insertando carreras de prueba...")
        carrera1 = CarreraModel(
            nombre="Ingeniería de Software",
            costo=4500000.0,
            semestres=10,
            modalidad="Presencial",
            facultad="Ingeniería"
        )
        carrera2 = CarreraModel(
            nombre="Ingeniería de Sistemas",
            costo=4200000.0,
            semestres=10,
            modalidad="Virtual",
            facultad="Ingeniería"
        )
        
        session.add_all([carrera1, carrera2])
        session.commit() # Guardamos los cambios en la base de datos

        print("Insertando estudiantes de prueba...")
        estudiante1 = EstudianteModel(
            documento="1001234567",
            nombres="Ana María",
            apellidos="Gómez Pérez",
            correo="ana.gomez@umb.edu.co",
            semestre=5,
            id_carrera=carrera1.id_carrera
        )
        estudiante2 = EstudianteModel(
            documento="1009876543",
            nombres="Carlos Andrés",
            apellidos="Rodríguez",
            correo="carlos.rodriguez@umb.edu.co",
            semestre=3,
            id_carrera=carrera2.id_carrera
        )

        session.add_all([estudiante1, estudiante2])
        session.commit()

        print("¡Datos de prueba insertados con éxito en MySQL Workbench!")

    except Exception as e:
        session.rollback()
        print("Ocurrió un error al insertar los datos:", e)
    finally:
        session.close()

if __name__ == "__main__":
    seed_database()
    