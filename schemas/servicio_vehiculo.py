"""
Schemas Pydantic para historial de servicios aplicados a vehículos.
"""

from typing import Optional
from datetime import datetime, date, time
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field, ConfigDict


class EstadoSolicitud(str, Enum):
    PROGRAMADA = "Programada"
    PROCESO    = "Proceso"
    REALIZADA  = "Realizada"
    CANCELADA  = "Cancelada"


# =========================================================
# Schemas anidados para la respuesta
# =========================================================

class VehiculoEnOrden(BaseModel):
    id_vehiculo: int
    placas: Optional[str]
    marca: str
    modelo: str
    color: Optional[str]
    model_config = ConfigDict(from_attributes=True)


class ServicioEnOrden(BaseModel):
    id_servicio: int
    nombre_servicio: str
    descripcion_servicio: Optional[str]
    precio: Decimal
    model_config = ConfigDict(from_attributes=True)


class UsuarioEnOrden(BaseModel):
    id_usuario: int
    nombre_usuario: str
    correo_usuario: str
    model_config = ConfigDict(from_attributes=True)


# =========================================================
# Create (POST)
# El cajero debe tener rol 3, el operativo rol 4.
# Puedes mandar id o nombre (o ambos).
# =========================================================

class ServicioVehiculoCreate(BaseModel):
    id_vehiculo: int = Field(..., gt=0)
    id_servicio: int = Field(..., gt=0)

    id_cajero:     Optional[int] = Field(None, description="ID del usuario con rol Cajero (rol 3)")
    nombre_cajero: Optional[str] = Field(None, description="Nombre del usuario con rol Cajero (rol 3)")

    id_operativo:     Optional[int] = Field(None, description="ID del usuario con rol Operativo (rol 4)")
    nombre_operativo: Optional[str] = Field(None, description="Nombre del usuario con rol Operativo (rol 4)")

    fecha:   Optional[date] = None
    hora:    Optional[time] = None
    estatus: EstadoSolicitud = EstadoSolicitud.PROGRAMADA


# =========================================================
# Update (PUT)
# =========================================================

class ServicioVehiculoUpdate(BaseModel):
    id_cajero:        Optional[int] = None
    nombre_cajero:    Optional[str] = None
    id_operativo:     Optional[int] = None
    nombre_operativo: Optional[str] = None
    fecha:   Optional[date] = None
    hora:    Optional[time] = None
    estatus: Optional[EstadoSolicitud] = None
    estatus_servicio_vehiculo: Optional[bool] = None


# =========================================================
# Response (GET)
# =========================================================

class ServicioVehiculoRead(BaseModel):
    id_servicio_vehiculo: int
    id_vehiculo:  int
    id_servicio:  int
    id_cajero:    int
    id_operativo: int
    fecha:   Optional[date]
    hora:    Optional[time]
    estatus: EstadoSolicitud
    estatus_servicio_vehiculo: Optional[bool]
    fecha_servicio:      Optional[datetime]
    fecha_registro:      Optional[datetime]
    fecha_actualizacion: Optional[datetime]

    vehiculo:  Optional[VehiculoEnOrden] = None
    servicio:  Optional[ServicioEnOrden] = None
    cajero:    Optional[UsuarioEnOrden]  = None
    operativo: Optional[UsuarioEnOrden]  = None

    model_config = ConfigDict(from_attributes=True)