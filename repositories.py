from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from models import CarreraModel, EstudianteModel, CandidatoModel

class CarreraRepository:
    """Repositorio CRUD para la entidad Carrera"""
    def __init__(self, db: Session):
        self.db = db

    def crear(self, nombre: str, costo: float, semestres: int, modalidad: str, facultad: str):
        carrera = CarreraModel(nombre=nombre, costo=costo, semestres=semestres, modalidad=modalidad, facultad=facultad)
        self.db.add(carrera)
        self.db.commit()
        self.db.refresh(carrera)
        return carrera

    def obtener_todos(self):
        return self.db.query(CarreraModel).all()

    def actualizar(self, id_carrera: int, nuevo_nombre: str):
        carrera = self.db.query(CarreraModel).filter(CarreraModel.id_carrera == id_carrera).first()
        if carrera:
            carrera.nombre = nuevo_nombre
            self.db.commit()
        return carrera

    def eliminar(self, id_carrera: int):
        carrera = self.db.query(CarreraModel).filter(CarreraModel.id_carrera == id_carrera).first()
        if carrera:
            self.db.delete(carrera)
            self.db.commit()
        return carrera


class EstudianteRepository:
    """Repositorio CRUD para Estudiante + Solución de Consulta N+1 con JOIN"""
    def __init__(self, db: Session):
        self.db = db

    def crear(self, documento: str, nombres: str, apellidos: str, correo: str, semestre: int, id_carrera: int):
        estudiante = EstudianteModel(
            documento=documento, nombres=nombres, apellidos=apellidos, 
            correo=correo, semestre=semestre, id_carrera=id_carrera
        )
        self.db.add(estudiante)
        self.db.commit()
        self.db.refresh(estudiante)
        return estudiante

    def obtener_todos(self):
        return self.db.query(EstudianteModel).all()

    # ⭐ AQUÍ ESTÁ LA SOLUCIÓN AL PROBLEMA N+1 USANDO JOIN (joinedload) ⭐
    def obtener_estudiantes_con_carrera_join(self):
        """
        Trae los estudiantes junto con su respectiva carrera en UNA SOLA consulta SQL,
        evitando que el ORM ejecute una consulta independiente por cada estudiante (Problema N+1).
        """
        return self.db.query(EstudianteModel).options(joinedload(EstudianteModel.carrera)).all()


class CandidatoRepository:
    """Repositorio CRUD para la entidad Candidato"""
    def __init__(self, db: Session):
        self.db = db

    def crear(self, nombre_planeta: str, propuestas: str, numero_tarjeton: int, id_estudiante: int):
        candidato = CandidatoModel(
            nombre_planeta=nombre_planeta, propuestas=propuestas, 
            numero_tarjeton=numero_tarjeton, id_estudiante=id_estudiante
        )
        self.db.add(candidato)
        self.db.commit()
        self.db.refresh(candidato)
        return candidato

    def obtener_todos(self):
        return self.db.query(CandidatoModel).all()