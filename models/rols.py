"""
Modelo ORM de la tabla de roles.
"""

from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from models.base import Base


# pylint: disable=too-few-public-methods
class Rol(Base):
    """
    Representa los roles dentro del sistema.
    Ejemplo: Administrador, Empleado, Cajero, etc.

    Atributos:
        id_rol (int): ID único del rol.
        nombre_rol (str): Nombre del rol.
        descripcion_rol (str | None): Descripción del rol.
        fecha_creacion (datetime): Fecha de creación del registro.
        fecha_actualizacion (datetime): Fecha de última actualización.
        usuarios (List[User]): Usuarios asociados a este rol.
    """

    __tablename__ = "roles"

    # =========================================================
    # 🔹 Columnas
    # =========================================================

    id_rol = Column(Integer, primary_key=True, index=True)

    nombre_rol = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    descripcion_rol = Column(
        String(150),
        nullable=True
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

    # =========================================================
    # 🔹 Relaciones
    # =========================================================

    # Un rol puede tener muchos usuarios
    usuarios = relationship(
        "User",
        back_populates="rol",
        cascade="all, delete-orphan"
    )

    # =========================================================
    # 🔹 Representación
    # =========================================================

    def __repr__(self) -> str:
        """
        Representación en string del rol.
        """
        return (
            f"<Rol(id={self.id_rol}, "
            f"nombre='{self.nombre_rol}')>"
        )
