"""
Endpoints CRUD para Productos.
GET    /productos/       -> lista todos
GET    /productos/{id}   -> obtiene uno por ID
POST   /productos/       -> crea un nuevo producto
PUT    /productos/{id}   -> actualiza un producto existente
DELETE /productos/{id}   -> elimina un producto
"""

from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.session import get_db
from models.producto import Producto
from models.user import User
from models.servicio import Servicio
from schemas.producto import ProductoCreate, ProductoUpdate, ProductoResponse
from core.security import get_current_user

router = APIRouter(
    prefix="/productos",
    tags=["Productos"],
)


def _calcular_precio_final(precio: Decimal, descuento_porcentaje: Decimal) -> Decimal:
    descuento_monto = precio * (descuento_porcentaje / Decimal("100"))
    return round(precio - descuento_monto, 2)


def _get_or_404(db: Session, producto_id: int) -> Producto:
    producto = db.query(Producto).filter(Producto.id_producto == producto_id).first()
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto con id {producto_id} no encontrado",
        )
    return producto


# GET /productos/
@router.get("/", response_model=list[ProductoResponse])
def get_productos(
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return db.query(Producto).all()


# GET /productos/{id}
@router.get("/{producto_id}", response_model=ProductoResponse)
def get_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    return _get_or_404(db, producto_id)


# POST /productos/
@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def create_producto(
    datos: ProductoCreate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    if not db.query(Servicio).filter(Servicio.id_servicio == datos.id_servicio).first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Servicio con id {datos.id_servicio} no encontrado",
        )

    nuevo = Producto(
        nombre_producto=datos.nombre_producto,
        descripcion_producto=datos.descripcion_producto,
        precio=datos.precio,
        descuento_porcentaje=datos.descuento_porcentaje,
        stock=datos.stock,
        unidad_medida=datos.unidad_medida,
        estatus_producto=datos.estatus_producto,
        precio_final=_calcular_precio_final(datos.precio, datos.descuento_porcentaje),
        id_servicio=datos.id_servicio,
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo


# PUT /productos/{id}
@router.put("/{producto_id}", response_model=ProductoResponse)
def update_producto(
    producto_id: int,
    datos: ProductoUpdate,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    producto = _get_or_404(db, producto_id)

    if datos.id_servicio is not None:
        if not db.query(Servicio).filter(Servicio.id_servicio == datos.id_servicio).first():
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Servicio con id {datos.id_servicio} no encontrado",
            )
        producto.id_servicio = datos.id_servicio

    if datos.nombre_producto is not None:
        producto.nombre_producto = datos.nombre_producto
    if datos.descripcion_producto is not None:
        producto.descripcion_producto = datos.descripcion_producto
    if datos.stock is not None:
        producto.stock = datos.stock
    if datos.unidad_medida is not None:
        producto.unidad_medida = datos.unidad_medida
    if datos.estatus_producto is not None:
        producto.estatus_producto = datos.estatus_producto

    nuevo_precio = datos.precio if datos.precio is not None else producto.precio
    nuevo_descuento = datos.descuento_porcentaje if datos.descuento_porcentaje is not None else producto.descuento_porcentaje

    if datos.precio is not None or datos.descuento_porcentaje is not None:
        producto.precio = nuevo_precio
        producto.descuento_porcentaje = nuevo_descuento
        producto.precio_final = _calcular_precio_final(nuevo_precio, nuevo_descuento)

    db.commit()
    db.refresh(producto)
    return producto


# DELETE /productos/{id}
@router.delete("/{producto_id}", status_code=status.HTTP_200_OK)
def delete_producto(
    producto_id: int,
    db: Session = Depends(get_db),
    _current_user: User = Depends(get_current_user),
):
    producto = _get_or_404(db, producto_id)
    db.delete(producto)
    db.commit()
    return {"mensaje": f"Producto con id {producto_id} eliminado correctamente"}