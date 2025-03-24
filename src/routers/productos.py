from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db import dependencies
from .schemas import schemas, crud

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.post("/", response_model=schemas.ProductoResponse)
def crear_producto(
    producto: schemas.ProductoCreate, db: Session = Depends(dependencies.get_db)
):
    return crud.crear_producto(db, producto)


@router.get("/", response_model=List[schemas.ProductoResponse])
def listar_productos(db: Session = Depends(dependencies.get_db)):
    return crud.listar_productos(db)


@router.get("/{producto_id}", response_model=schemas.ProductoResponse)
def obtener_producto(producto_id: int, db: Session = Depends(dependencies.get_db)):
    producto = crud.obtener_producto(db, producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.put("/{producto_id}", response_model=schemas.ProductoResponse)
def actualizar_producto(
    producto_id: int,
    producto: schemas.ProductoCreate,
    db: Session = Depends(dependencies.get_db),
):
    producto_actualizado = crud.actualizar_producto(db, producto_id, producto)
    if not producto_actualizado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto_actualizado


@router.delete("/{producto_id}", response_model=dict)
def eliminar_producto(producto_id: int, db: Session = Depends(dependencies.get_db)):
    if not crud.eliminar_producto(db, producto_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": "Producto eliminado exitosamente"}
