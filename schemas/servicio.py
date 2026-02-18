"""
Schemas Pydantic para la entidad Servicio.
Representa el catálogo de servicios del autolavado.
"""

from typing import Optional
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


# =========================================================
# 🔹 Base
# =========================================================

class ServicioBase(BaseModel):
    """
    Atributos requeridos para registrar un servicio.
    """

    nombre_servicio: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nombre del servicio"
    )

    descripcion_servicio: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Descripción opcional del servicio"
    )

    precio: Decimal = Field(
        ...,
        gt=0,
        description="Precio del servicio"
    )

    duracion_minutos: Optional[int] = Field(
        default=None,
        gt=0,
        description="Duración estimada en minutos"
    )

    estatus_servicio: bool = Field(
        default=True,
        description="Indica si el servicio está activo"
    )


# =========================================================
# 🔹 Create
# =========================================================

class ServicioCreate(ServicioBase):
    """
    Datos requeridos para registrar un nuevo servicio.
    """
    # 'pass' eliminado: ya hereda todo de ServicioBase


# =========================================================
# 🔹 Update
# =========================================================

class ServicioUpdate(BaseModel):
    """
    Datos permitidos para actualizar un servicio.
    Todos los campos son opcionales.
    """

    nombre_servicio: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    descripcion_servicio: Optional[str] = Field(
        default=None,
        max_length=200
    )

    precio: Optional[Decimal] = Field(
        default=None,
        gt=0
    )

    duracion_minutos: Optional[int] = Field(
        default=None,
        gt=0
    )

    estatus_servicio: Optional[bool] = None


# =========================================================
# 🔹 Read (Response)
# =========================================================

class ServicioRead(ServicioBase):
    """
    Datos devueltos para consultar un servicio.
    """

    id_servicio: int
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True
    )
