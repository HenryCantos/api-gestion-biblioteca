from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base

# Cambiamos la URL para que apunte al archivo local SQLite 'biblioteca.db'
DATABASE_URL = "sqlite:///./biblioteca.db"

# Agregamos connect_args para permitir que funcione correctamente con FastAPI
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()