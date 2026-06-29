from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.database import engine, SessionLocal

# Importaciones modulares con la arquitectura app/ limpia
import app.models as models
import app.crud as crud
import app.schemas as schemas
from app.database import engine, SessionLocal

# Crear automáticamente las tablas en la base de datos al arrancar
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API Gestión Biblioteca - UG",
    description="CRUD completo y endpoints de búsqueda para la gestión de Libros",
    version="1.0"
)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ENDPOINTS DE GESTIÓN (CRUD) ---

@app.post("/libros")
def crear_libro(libro: schemas.LibroCreate, db: Session = Depends(get_db)):
    existe = db.query(models.Libro).filter(models.Libro.isbn == libro.isbn).first()
    if existe:
        raise HTTPException(status_code=400, detail="ISBN ya registrado")
    return crud.crear_libro(db, libro)

@app.get("/libros")
def listar_libros(db: Session = Depends(get_db)):
    return crud.obtener_libros(db)

@app.get("/libros/{id}")
def obtener_libro(id: int, db: Session = Depends(get_db)):
    libro = crud.obtener_libro(db, id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return libro

@app.put("/libros/{id}")
def actualizar_libro(id: int, datos: schemas.LibroUpdate, db: Session = Depends(get_db)):
    libro = crud.obtener_libro(db, id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    
    isbn_existente = db.query(models.Libro).filter(
        models.Libro.isbn == datos.isbn,
        models.Libro.id != id
    ).first()
    if isbn_existente:
        raise HTTPException(status_code=400, detail="ISBN ya registrado por otro libro")
        
    return crud.actualizar_libro(db, id, datos)

@app.delete("/libros/{id}")
def eliminar_libro(id: int, db: Session = Depends(get_db)):
    libro = crud.eliminar_libro(db, id)
    if not libro:
        raise HTTPException(status_code=404, detail="Libro no encontrado")
    return {"mensaje": "Libro eliminado con éxito"}

# --- ENDPOINTS DE BÚSQUEDA AVANZADA ---

@app.get("/buscar/titulo/{titulo}")
def buscar_titulo(titulo: str, db: Session = Depends(get_db)):
    return db.query(models.Libro).filter(models.Libro.titulo.ilike(f"%{titulo}%")).all()

@app.get("/buscar/autor/{autor}")
def buscar_autor(autor: str, db: Session = Depends(get_db)):
    return db.query(models.Libro).filter(models.Libro.autor.ilike(f"%{autor}%")).all()

@app.get("/buscar/isbn/{isbn}")
def buscar_isbn(isbn: str, db: Session = Depends(get_db)):
    return db.query(models.Libro).filter(models.Libro.isbn == isbn).first()