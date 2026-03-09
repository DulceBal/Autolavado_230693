"""
Modelo ORM de usuarios.
Representa los usuarios que pueden acceder al sistema.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    func
)
from sqlalchemy.orm import relationship

from models.base import Base


# pylint: disable=too-few-public-methods
class User(Base):
    """
    Representa los usuarios del sistema.
    Ejemplo: Administrador, Empleado, Cajero.

    Atributos:
        id_usuario (int): ID único del usuario.
        nombre_usuario (str): Nombre del usuario.
        correo_usuario (str): Correo electrónico único.
        password_usuario (str): Contraseña hasheada.
        activo (bool): Soft delete / activo.
        id_rol (int): FK hacia la tabla roles.
        fecha_creacion (datetime): Fecha de creación del registro.
        fecha_actualizacion (datetime): Fecha de última actualización.
        rol (Rol): Relación con la tabla de roles.
    """

    __tablename__ = "users"

    id_usuario = Column(
        Integer,
        primary_key=True,
        index=True
    )
    nombre_usuario = Column(
        String(100),
        nullable=False,
        index=True
    )
    correo_usuario = Column(
        String(150),
        unique=True,
        nullable=False,
        index=True
    )
    password_usuario = Column(
        String(255),
        nullable=False
    )
    activo = Column(
        Boolean,
        default=True
    )
    id_rol = Column(
        Integer,
        ForeignKey("roles.id_rol", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    fecha_creacion = Column(
        DateTime(timezone=True),
        server_default=func.now(),  # pylint: disable=not-callable
    )
    fecha_actualizacion = Column(
        DateTime(timezone=True),
        server_default=func.now(),  # pylint: disable=not-callable
        onupdate=func.now()          # pylint: disable=not-callable
    )

    rol = relationship("Rol", back_populates="usuarios")

    def __repr__(self) -> str:
        """Representación en string del usuario."""
        return (
            f"<User(id_usuario={self.id_usuario}, "
            f"nombre_usuario='{self.nombre_usuario}', "
            f"correo_usuario='{self.correo_usuario}', "
            f"id_rol={self.id_rol})>"
        )      