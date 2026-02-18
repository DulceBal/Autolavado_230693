"""
Schemas Pydantic para la entidad Rol.
Definen validación y serialización de datos en la API.
"""

from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


# =========================================================
# 🔹 Base
# =========================================================

class RolBase(BaseModel):
    """
    Atributos comunes del rol.
    """

    nombre_rol: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Nombre del rol (ej. Administrador, Empleado)"
    )

    descripcion_rol: Optional[str] = Field(
        default=None,
        max_length=150,
        description="Descripción opcional del rol"
    )


# =========================================================
# 🔹 Create
# =========================================================

class RolCreate(RolBase):
    """
    Datos requeridos para registrar un nuevo rol.
    """
    # 'pass' eliminado: ya hereda todo de RolBase


# =========================================================
# 🔹 Update
# =========================================================

class RolUpdate(BaseModel):
    """
    Datos permitidos para actualizar un rol.
    Todos los campos son opcionales.
    """

    nombre_rol: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50
    )

    descripcion_rol: Optional[str] = Field(
        default=None,
        max_length=150
    )


# =========================================================
# 🔹 Read (Response)
# =========================================================

class RolRead(RolBase):
    """
    Datos devueltos por la API al consultar roles.
    """

    id_rol: int
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True
    )
