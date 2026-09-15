from database import SessionLocal
from repositories import EstudianteRepository

session = SessionLocal()
repo = EstudianteRepository(session)

# Ejecutamos la consulta con JOIN optimizada para evitar N+1
print("--- Consultando estudiantes con JOIN (Evitando N+1) ---")
estudiantes = repo.obtener_estudiantes_con_carrera_join()

for est in estudiantes:
    # Gracias al JOIN, podemos acceder a est.carrera.nombre sin hacer consultas extra a la BD
    print(f"Estudiante: {est.nombres} {est.apellidos} - Carrera: {est.carrera.nombre}")

session.close()