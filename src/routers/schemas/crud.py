from sqlalchemy.orm import Session
from .models import Producto
from .schemas import ProductoCreate


def crear_producto(db: Session, producto: ProductoCreate):
    nuevo_producto = Producto(**producto.model_dump())
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto


def listar_productos(db: Session):
    return db.query(Producto).all()


def obtener_producto(db: Session, producto_id: int):
    return db.query(Producto).filter(Producto.id == producto_id).first()


def actualizar_producto(db: Session, producto_id: int, producto: ProductoCreate):
    producto_db = obtener_producto(db, producto_id)
    if not producto_db:
        return None
    for key, value in producto.model_dump().items():
        setattr(producto_db, key, value)
    db.commit()
    db.refresh(producto_db)
    return producto_db


def eliminar_producto(db: Session, producto_id: int):
    producto_db = obtener_producto(db, producto_id)
    if not producto_db:
        return None
    db.delete(producto_db)
    db.commit()
    return True
