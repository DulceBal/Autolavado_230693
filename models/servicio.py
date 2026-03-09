"""
Modelo ORM de servicios del autolavado.
Representa el catálogo de servicios disponibles.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Boolean,
    DateTime,
    func
)
from sqlalchemy.orm import relationship

from models.base import Base


# pylint: disable=too-few-public-methods
class Servicio(Base):
    """
    Catálogo de servicios disponibles.
    Ejemplo: Lavado básico, Encerado, Lavado premium, etc.

    Atributos:
        id_servicio (int): ID único del servicio.
        nombre_servicio (str): Nombre del servicio.
        descripcion_servicio (str | None): Descripción del servicio.
        precio (Decimal): Precio del servicio.
        duracion_minutos (int | None): Duración estimada en minutos.
        estatus_servicio (bool): Soft delete / activo.
        fecha_creacion (datetime): Fecha de creación del registro.
        fecha_actualizacion (datetime): Fecha de última actualización.
        vehiculos (List[ServicioVehiculo]): Servicios aplicados a vehículos.
    """

    __tablename__ = "servicios"

    # =========================================================
    # 🔹 Columnas principales
    # =========================================================

    id_servicio = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )

    nombre_servicio = Column(
        String(100),
        nullable=False,
        index=True
    )

    descripcion_servicio = Column(
        String(200),
        nullable=True
    )

    precio = Column(
        Numeric(10, 2),
        nullable=False
    )

    duracion_minutos = Column(
        Integer,
        nullable=True
    )

    estatus_servicio = Column(
        Boolean,
        default=True
    )

    # =========================================================
    # 🔹 Auditoría
    # =========================================================

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

    vehiculos = relationship(
        "ServicioVehiculo",
        back_populates="servicio",
        cascade="all, delete-orphan"
    )

    productos = relationship("Producto", back_populates="servicio")

    # =========================================================
    # 🔹 Representación
    # =========================================================

    def __repr__(self) -> str:
        """
        Representación en string del servicio.
        """
        return (
            f"<Servicio(id={self.id_servicio}, "
            f"nombre='{self.nombre_servicio}', "
            f"precio={self.precio})>"
        )
        