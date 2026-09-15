from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class CarreraModel(Base):
    __tablename__ = 'carrera'
    
    id_carrera = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    costo = Column(Float, nullable=False)
    semestres = Column(Integer, nullable=False)
    modalidad = Column(String(50), nullable=False)
    facultad = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)

    # Relación: Una carrera tiene muchos estudiantes
    estudiantes = relationship("EstudianteModel", back_populates="carrera")


class EstudianteModel(Base):
    __tablename__ = 'estudiante'
    
    id_estudiante = Column(Integer, primary_key=True, autoincrement=True)
    documento = Column(String(20), unique=True, nullable=False)
    nombres = Column(String(100), nullable=False)
    apellidos = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    semestre = Column(Integer, nullable=False)
    id_carrera = Column(Integer, ForeignKey('carrera.id_carrera'), nullable=False)

    # Relaciones
    carrera = relationship("CarreraModel", back_populates="estudiantes")
    votos = relationship("VotoAuditoriaModel", back_populates="estudiante")


class CandidatoModel(Base):
    __tablename__ = 'candidato'
    
    id_candidato = Column(Integer, primary_key=True, autoincrement=True)
    nombre_planeta = Column(String(100), nullable=False)
    propuestas = Column(String(500), nullable=False)
    numero_tarjeton = Column(Integer, unique=True, nullable=False)
    id_estudiante = Column(Integer, ForeignKey('estudiante.id_estudiante'), nullable=False)

    # Relación con conteo de resultados
    resultados = relationship("ConteoResultadosModel", back_populates="candidato")

class VotoAuditoriaModel(Base):
    __tablename__ = 'voto_auditoria'
    
    id_voto = Column(Integer, primary_key=True, autoincrement=True)
    fecha_hora = Column(DateTime, default=datetime.utcnow, nullable=False)
    hash_verificacion = Column(String(255), unique=True, nullable=False)
    id_estudiante = Column(Integer, ForeignKey('estudiante.id_estudiante'), nullable=False)

    # Relación
    estudiante = relationship("EstudianteModel", back_populates="votos")


class ConteoResultadosModel(Base):
    __tablename__ = 'conteo_resultados'
    
    id_conteo = Column(Integer, primary_key=True, autoincrement=True)
    total_votos = Column(Integer, default=0, nullable=False)
    id_candidato = Column(Integer, ForeignKey('candidato.id_candidato'), nullable=False)

    # Relación
    candidato = relationship("CandidatoModel", back_populates="resultados")
