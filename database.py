import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker

# Carga las variables de entorno desde el archivo .env
load_dotenv()

# Lee los datos de conexión o asigna valores por defecto
USER = os.getenv("DB_USER", "root")
PASSWORD = os.getenv("DB_PASSWORD", "")
HOST = os.getenv("DB_HOST", "localhost")
PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "sistema_votacion_estudiantil")

# Configura la conexión a MySQL de forma segura
DATABASE_URL = URL.create(
    "mysql+pymysql",
    username=USER,
    password=PASSWORD,
    host=HOST,
    port=int(PORT),
    database=DB_NAME
)

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from models import Base

# Crea automáticamente las tablas en MySQL si aún no existen
Base.metadata.create_all(bind=engine)