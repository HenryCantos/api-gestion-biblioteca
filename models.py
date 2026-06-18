from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Boolean
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    rol = Column(String(20), nullable=False)
    prestamos = relationship(
        "Prestamo",
        back_populates="usuario"
    )

class Libro(Base):
    __tablename__ = "libros"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(200), nullable=False)
    autor = Column(String(150), nullable=False)
    isbn = Column(String(20), unique=True, nullable=False)
    stock = Column(Integer, nullable=False)
    prestamos = relationship(
        "Prestamo",
        back_populates="libro"
    )

class Prestamo(Base):
    __tablename__ = "prestamos"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(
        Integer,
        ForeignKey("usuarios.id")
    )
    libro_id = Column(
        Integer,
        ForeignKey("libros.id")
    )
    fecha_prestamo = Column(Date)
    fecha_devolucion_maxima = Column(Date)
    devuelto = Column(
        Boolean,
        default=False
    )
    usuario = relationship(
        "Usuario",
        back_populates="prestamos"
    )
    libro = relationship(
        "Libro",
        back_populates="prestamos"
    )

