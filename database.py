from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./biblioteca.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# AQUÍ CREAMOS LA BASE
Base = declarative_base()

def init_db():
    # IMPORTAMOS DENTRO DE LA FUNCIÓN para romper el ciclo
    from models import Prestamo
    Base.metadata.create_all(bind=engine)