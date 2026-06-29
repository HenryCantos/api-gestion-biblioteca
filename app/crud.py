from sqlalchemy.orm import Session
from .models import Libro

def crear_libro(db: Session, datos):
    libro = Libro(
        titulo=datos.titulo,
        autor=datos.autor,
        isbn=datos.isbn,
        stock=datos.stock
    )

    db.add(libro)
    db.commit()
    db.refresh(libro)

    return libro

def obtener_libros(db: Session):
    return db.query(Libro).all()

def obtener_libro(db: Session, libro_id: int):
    return db.query(Libro).filter(
        Libro.id == libro_id
    ).first()

def actualizar_libro(
    db,
    libro_id: int,
    datos
):
    libro = db.query(Libro).filter(
        Libro.id == libro_id
    ).first()

    if libro:

        libro.titulo = datos.titulo
        libro.autor = datos.autor
        libro.isbn = datos.isbn
        libro.stock = datos.stock

        db.commit()
        db.refresh(libro)

    return libro

def eliminar_libro(db: Session, libro_id: int):
    libro = obtener_libro(db, libro_id)

    if libro:
        db.delete(libro)
        db.commit()

    return libro

