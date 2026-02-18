"""
Schemas Pydantic para historial de servicios aplicados a vehículos.
Representa la operación o venta dentro del sistema.
"""

from typing import Optional
from datetime import datetime, date, time
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict


# =========================================================
# 🔹 ENUM (Debe coincidir con el modelo ORM)
# =========================================================

class EstadoSolicitud(str, Enum):
    """Posibles estados para una solicitud de servicio."""
    PROGRAMADA = "Programada"
    PROCESO = "Proceso"
    REALIZADA = "Realizada"
    CANCELADA = "Cancelada"


# =========================================================
# 🔹 Base
# =========================================================

class ServicioVehiculoBase(BaseModel):
    """
    Datos base para registrar un servicio aplicado a un vehículo.
    """

    id_vehiculo: int = Field(..., gt=0)
    id_servicio: int = Field(..., gt=0)

    fecha: Optional[date] = None
    hora: Optional[time] = None

    estatus: EstadoSolicitud = EstadoSolicitud.PROGRAMADA


# =========================================================
# 🔹 Create
# =========================================================

class ServicioVehiculoCreate(ServicioVehiculoBase):
    """
    Datos requeridos para registrar un nuevo servicio.
    """
    # 'pass' eliminado: ya hereda todo de ServicioVehiculoBase


# =========================================================
# 🔹 Update
# =========================================================

class ServicioVehiculoUpdate(BaseModel):
    """
    Datos permitidos para actualizar un servicio aplicado.
    Todos los campos son opcionales.
    """

    fecha: Optional[date] = None
    hora: Optional[time] = None
    estatus: Optional[EstadoSolicitud] = None
    estatus_servicio_vehiculo: Optional[bool] = None


# =========================================================
# 🔹 Read (Response)
# =========================================================

class ServicioVehiculoRead(ServicioVehiculoBase):
    """
    Datos devueltos al consultar el historial de servicios.
    """

    id_servicio_vehiculo: int
    fecha_servicio: datetime
    fecha_registro: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True
    )
