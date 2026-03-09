"""
Esquemas Pydantic para la entidad Cliente.
Definen la validación y serialización de datos en la API.
"""

from typing import Optional
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, ConfigDict


# =========================================================
# 🔹 Base
# =========================================================

class ClienteBase(BaseModel):
    """
    Atributos comunes del cliente.
    """

    nombre_cliente: str = Field(
        ...,
        min_length=2,
        max_length=120,
        description="Nombre completo del cliente"
    )

    telefono_cliente: Optional[str] = Field(
        default=None,
        max_length=20,
        description="Número telefónico del cliente"
    )

    email_cliente: Optional[EmailStr] = Field(
        default=None,
        max_length=120,
        description="Correo electrónico del cliente"
    )

    estatus_cliente: bool = Field(
        default=True,
        description="Indica si el cliente está activo"
    )


# =========================================================
# 🔹 Create
# =========================================================

class ClienteCreate(ClienteBase):
    """
    Datos requeridos para registrar un nuevo cliente.
    """
    # No se necesita 'pass' aquí


# =========================================================
# 🔹 Update
# =========================================================

class ClienteUpdate(BaseModel):
    """
    Datos permitidos para actualizar un cliente.
    Todos los campos son opcionales.
    """

    nombre_cliente: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=120
    )

    telefono_cliente: Optional[str] = Field(
        default=None,
        max_length=20
    )

    email_cliente: Optional[EmailStr] = Field(
        default=None,
        max_length=120
    )

    estatus_cliente: Optional[bool] = None


# =========================================================
# 🔹 Read (Response)
# =========================================================

class ClienteRead(ClienteBase):
    """
    Datos devueltos por la API al consultar clientes.
    """

    id_cliente: int
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True
    )


