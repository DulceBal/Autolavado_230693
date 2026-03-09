"""
Schemas Pydantic para el modelo Producto.
"""

from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime


class ProductoBase(BaseModel):
    nombre_producto: str = Field(..., max_length=150, example="Shampoo cera")
    descripcion_producto: Optional[str] = Field(None, max_length=300, example="Shampoo para interior")
    precio: Decimal = Field(..., ge=0, example=120.00)
    descuento_porcentaje: Decimal = Field(default=Decimal("0.00"), ge=0, le=100, example=10.00)
    stock: int = Field(..., ge=0, example=50)
    unidad_medida: str = Field(default="pieza", max_length=50, example="pieza")
    estatus_producto: bool = Field(default=True)
    id_servicio: int = Field(..., example=2)


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    nombre_producto: Optional[str] = Field(None, max_length=150)
    descripcion_producto: Optional[str] = Field(None, max_length=300)
    precio: Optional[Decimal] = Field(None, ge=0)
    descuento_porcentaje: Optional[Decimal] = Field(None, ge=0, le=100)
    stock: Optional[int] = Field(None, ge=0)
    unidad_medida: Optional[str] = Field(None, max_length=50)
    estatus_producto: Optional[bool] = None
    id_servicio: Optional[int] = None


class ProductoResponse(BaseModel):
    id_producto: int
    nombre_producto: str
    descripcion_producto: Optional[str]
    precio: Decimal
    descuento_porcentaje: Decimal
    stock: int
    unidad_medida: str
    estatus_producto: bool
    precio_final: Decimal
    id_servicio: int
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    class Config:
        from_attributes = True