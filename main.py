from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import crud
import schemas

from database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Gestión Biblioteca",
    description="CRUD de Libros",
    version="1.0"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/libros")
def crear_libro(
    libro: schemas.LibroCreate,
    db: Session = Depends(get_db)
):
    existe = db.query(models.Libro).filter(
        models.Libro.isbn == libro.isbn
    ).first()

    if existe:
        raise HTTPException(
            status_code=400,
            detail="ISBN ya registrado"
        )

    return crud.crear_libro(db, libro)


@app.get("/libros")
def listar_libros(
    db: Session = Depends(get_db)
):
    return crud.obtener_libros(db)


@app.get("/libros/{id}")
def obtener_libro(
    id: int,
    db: Session = Depends(get_db)
):
    libro = crud.obtener_libro(db, id)

    if not libro:
        raise HTTPException(
            status_code=404,
            detail="Libro no encontrado"
        )

    return libro

@app.put("/libros/{id}")
def actualizar_libro(
    id: int,
    datos: schemas.LibroUpdate,
    db: Session = Depends(get_db)
):

    libro = crud.obtener_libro(db, id)

    if not libro:
        raise HTTPException(
            status_code=404,
            detail="Libro no encontrado"
        )

    isbn_existente = db.query(models.Libro).filter(
        models.Libro.isbn == datos.isbn,
        models.Libro.id != id
    ).first()

    if isbn_existente:
        raise HTTPException(
            status_code=400,
            detail="ISBN ya registrado por otro libro"
        )

    return crud.actualizar_libro(
        db,
        id,
        datos
    )

@app.delete("/libros/{id}")
def eliminar_libro(
    id: int,
    db: Session = Depends(get_db)
):
    libro = crud.eliminar_libro(db, id)

    if not libro:
        raise HTTPException(
            status_code=404,
            detail="Libro no encontrado"
        )

    return {
        "mensaje": "Libro eliminado"
    }


@app.get("/buscar/titulo/{titulo}")
def buscar_titulo(
    titulo: str,
    db: Session = Depends(get_db)
):
    return db.query(models.Libro).filter(
        models.Libro.titulo.ilike(f"%{titulo}%")
    ).all()


@app.get("/buscar/autor/{autor}")
def buscar_autor(
    autor: str,
    db: Session = Depends(get_db)
):
    return db.query(models.Libro).filter(
        models.Libro.autor.ilike(f"%{autor}%")
    ).all()


@app.get("/buscar/isbn/{isbn}")
def buscar_isbn(
    isbn: str,
    db: Session = Depends(get_db)
):
    return db.query(models.Libro).filter(
        models.Libro.isbn == isbn
    ).first()


