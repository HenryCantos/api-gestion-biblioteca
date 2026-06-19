from fastapi import FastAPI
from database import init_db
from routers import prestamos

# Inicializamos la aplicación
app = FastAPI(title="Proyecto Biblioteca Melany")

# Inicializamos la base de datos al arrancar
@app.on_event("startup")
def startup_event():
    init_db()

# Registramos el router que creaste
app.include_router(prestamos.router)

# Ruta de prueba básica
@app.get("/")
def read_root():
    return {"message": "Bienvenido al sistema de biblioteca de Melany"}