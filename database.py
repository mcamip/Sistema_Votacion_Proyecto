from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configura tus datos de conexión a MySQL Workbench
USER = "root"
PASSWORD = "Luzetaitana2008."  # Cambia esto por tu contraseña de Workbench si tienes una
HOST = "localhost"
PORT = "3306"
DB_NAME = "sistema_votacion_estudiantil"

DATABASE_URL = f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
from models import Base
# Esto crea automáticamente las tablas en MySQL si aún no existen
Base.metadata.create_all(bind=engine)
