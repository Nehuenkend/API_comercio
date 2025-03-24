from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, ConfigDict
from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from typing import List

# Configuración de la base de datos
DATABASE_URL = "mysql+mysqlconnector://root:contraseña@localhost:3306/comercio"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Modelo de Producto
class Producto(Base):
    __tablename__ = "productos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255))
    precio = Column(Float)
    stock = Column(Integer)


# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Modelos Pydantic
class ProductoCreate(BaseModel):
    nombre: str
    precio: float
    stock: int


class ProductoResponse(ProductoCreate):
    id: int
    model_config = ConfigDict(from_attributes=True)


# Endpoints de Productos
@app.post("/productos/", response_model=ProductoResponse)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    nuevo_producto = Producto(**producto.model_dump())
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto


@app.get("/productos/", response_model=List[ProductoResponse])
def listar_productos(db: Session = Depends(get_db)):
    return db.query(Producto).all()


@app.get("/productos/{producto_id}", response_model=ProductoResponse)
def obtener_producto(producto_id: int, db: Session = Depends(get_db)):
    producto = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@app.put("/productos/{producto_id}", response_model=ProductoResponse)
def actualizar_producto(
    producto_id: int, producto: ProductoCreate, db: Session = Depends(get_db)
):
    producto_db = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto_db:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    for key, value in producto.model_dump().items():
        setattr(producto_db, key, value)
    db.commit()
    db.refresh(producto_db)
    return producto_db


@app.delete("/productos/{producto_id}", response_model=dict)
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    producto_db = db.query(Producto).filter(Producto.id == producto_id).first()
    if not producto_db:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    db.delete(producto_db)
    db.commit()
    return {"mensaje": "Producto eliminado exitosamente"}
