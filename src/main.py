from fastapi import FastAPI
from db.database import engine, Base
from routers import productos

# Crear tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Incluir routers
app.include_router(productos.router)
