import pytest
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

# 1. Configuración de la Base de Datos en Memoria para Pruebas (SQLite)
Base = declarative_base()

class CarreraModel(Base):
    __tablename__ = "carrera"
    id_carrera = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    costo = Column(Float, nullable=False)
    semestres = Column(Integer, nullable=False)
    modalidad = Column(String(50), nullable=False)
    facultad = Column(String(100), nullable=False)
    descripcion = Column(String(255), nullable=True)

class EstudianteModel(Base):
    __tablename__ = "estudiante"
    id_estudiante = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), nullable=False)

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

# --- PRUEBA 1: Inserción y validación de la Carrera (con la columna 'descripcion') ---
def test_crear_y_consultar_carrera(db_session):
    nueva_carrera = CarreraModel(
        nombre="Ingeniería de Software",
        costo=1500.0,
        semestres=9,
        modalidad="Virtual",
        facultad="Ingeniería",
        descripcion="Programa enfocado en desarrollo de software moderno y sistemas multicapa."
    )
    db_session.add(nueva_carrera)
    db_session.commit()

    carrera_db = db_session.query(CarreraModel).filter_by(nombre="Ingeniería de Software").first()
    assert carrera_db is not None
    assert carrera_db.descripcion == "Programa enfocado en desarrollo de software moderno y sistemas multicapa."

# --- PRUEBA 2: Registro y consulta de un Estudiante ---
def test_crear_y_consultar_estudiante(db_session):
    nuevo_estudiante = EstudianteModel(
        nombre="Carlos Pérez",
        correo="carlos.perez@umb.edu.co"
    )
    db_session.add(nuevo_estudiante)
    db_session.commit()

    estudiante_db = db_session.query(EstudianteModel).filter_by(correo="carlos.perez@umb.edu.co").first()
    assert estudiante_db is not None
    assert estudiante_db.nombre == "Carlos Pérez"

# --- PRUEBA 3: Conteo y listado de registros ---
def test_listar_multiples_carreras(db_session):
    c1 = CarreraModel(nombre="Ingeniería Civil", costo=1200.0, semestres=10, modalidad="Presencial", facultad="Ingeniería", descripcion="Infraestructura")
    c2 = CarreraModel(nombre="Administración", costo=1000.0, semestres=8, modalidad="Virtual", facultad="Negocios", descripcion="Gestión empresarial")
    
    db_session.add_all([c1, c2])
    db_session.commit()

    total_carreras = db_session.query(CarreraModel).count()
    assert total_carreras == 2
    