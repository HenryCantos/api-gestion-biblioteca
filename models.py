from sqlalchemy import Column, Integer, String
from database import Base # Esto está bien si Base vive en database

class Prestamo(Base):
    __tablename__ = "prestamos"
    id = Column(Integer, primary_key=True, index=True)
    libro_id = Column(Integer)
    usuario_id = Column(Integer)
    fecha_prestamo = Column(String)
    fecha_devolucion = Column(String)