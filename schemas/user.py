"""
Schemas Pydantic para la entidad Usuario.
Definen validación y serialización para la API.
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# =========================================================
# 🔹 Base
# =========================================================

class UserBase(BaseModel):
    """
    Atributos comunes del usuario.
    """

    nombre_usuario: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Nombre del usuario" 
    )

    correo_usuario: EmailStr = Field(
        ...,
        description="Correo electrónico único del usuario"
    )


# =========================================================
# 🔹 Create
# =========================================================

class UserCreate(UserBase):
    """
    Datos requeridos para registrar un nuevo usuario.
    """

    password_usuario: str = Field(
        ...,
        min_length=6,
        max_length=100,
        description="Contraseña en texto plano (será hasheada en backend)"
    )

    id_rol: int = Field(
        ...,
        gt=0,
        description="ID del rol asignado"
    )


# =========================================================
# 🔹 Update
# =========================================================

class UserUpdate(BaseModel):
    """
    Datos permitidos para actualizar un usuario.
    Todos los campos son opcionales.
    """

    nombre_usuario: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )

    correo_usuario: Optional[EmailStr] = None

    password_usuario: Optional[str] = Field(
        default=None,
        min_length=6,
        max_length=100
    )

    activo: Optional[bool] = None

    id_rol: Optional[int] = Field(
        default=None,
        gt=0
    )


# =========================================================
# 🔹 Read (Response)
# =========================================================

class UserRead(UserBase):
    """
    Datos devueltos al consultar usuarios.
    NO incluye contraseña.
    """

    id_usuario: int
    activo: bool
    id_rol: int

    model_config = ConfigDict(
        from_attributes=True
    )
