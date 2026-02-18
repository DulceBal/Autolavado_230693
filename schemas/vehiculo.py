"""
Schemas Pydantic para la entidad Vehículo.
Definen validación y serialización para la API.
"""

from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


# =========================================================
# 🔹 Base
# =========================================================

class VehiculoBase(BaseModel):
    """
    Atributos comunes del vehículo.
    """

    placas: str = Field(
        ...,
        min_length=3,
        max_length=20,
        description="Placas del vehículo (únicas)"
    )

    marca: str = Field(
        ...,
        min_length=2,
        max_length=60
    )

    modelo: str = Field(
        ...,
        min_length=1,
        max_length=60
    )

    color: Optional[str] = Field(
        default=None,
        max_length=40
    )

    tipo_vehiculo: Optional[str] = Field(
        default=None,
        max_length=50
    )

    id_cliente: int = Field(
        ...,
        gt=0,
        description="ID del cliente propietario"
    )

    estatus_vehiculo: bool = Field(
        default=True,
        description="Indica si el vehículo está activo"
    )


# =========================================================
# 🔹 Create
# =========================================================

class VehiculoCreate(VehiculoBase):
    """
    Datos requeridos para registrar un nuevo vehículo.
    """
    # 'pass' eliminado: hereda todo de VehiculoBase


# =========================================================
# 🔹 Update
# =========================================================

class VehiculoUpdate(BaseModel):
    """
    Datos permitidos para actualizar un vehículo.
    Todos los campos son opcionales.
    """

    placas: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=20
    )

    marca: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=60
    )

    modelo: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=60
    )

    color: Optional[str] = Field(
        default=None,
        max_length=40
    )

    tipo_vehiculo: Optional[str] = Field(
        default=None,
        max_length=50
    )

    id_cliente: Optional[int] = Field(
        default=None,
        gt=0
    )

    estatus_vehiculo: Optional[bool] = None


# =========================================================
# 🔹 Read (Response)
# =========================================================

class VehiculoRead(VehiculoBase):
    """
    Datos devueltos al consultar vehículos.
    """

    id_vehiculo: int
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
