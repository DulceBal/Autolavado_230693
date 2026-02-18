"""
Modelo ORM que registra los servicios aplicados a los vehículos.
(Representa la operación / venta)
"""

from enum import Enum as PyEnum

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    DateTime,
    Date,
    Time,
    Enum,
    Boolean,
    func,
)
from sqlalchemy.orm import relationship

from models.base import Base


# =========================================================
# 🔹 ENUM DE ESTADOS
# =========================================================

class EstadoSolicitud(PyEnum):
    """Posibles estados para una solicitud de servicio."""
    PROGRAMADA = "Programada"
    PROCESO = "Proceso"
    REALIZADA = "Realizada"
    CANCELADA = "Cancelada"


# pylint: disable=too-few-public-methods
class ServicioVehiculo(Base):
    """
    Registro de servicios aplicados a los vehículos.
    Representa una orden o venta dentro del sistema.

    Atributos:
        id_servicio_vehiculo (int): ID único del registro.
        id_vehiculo (int): FK hacia el vehículo.
        id_servicio (int): FK hacia el servicio.
        fecha (date | None): Fecha programada del servicio.
        hora (time | None): Hora programada del servicio.
        estatus (EstadoSolicitud): Estado del servicio.
        estatus_servicio_vehiculo (bool): Soft delete / activo.
        fecha_registro (datetime): Fecha de creación del registro.
        fecha_actualizacion (datetime): Fecha de última actualización.
        fecha_servicio (datetime): Fecha efectiva de realización del servicio.
        vehiculo (Vehiculo): Relación con Vehiculo.
        servicio (Servicio): Relación con Servicio.
    """

    __tablename__ = "servicio_vehiculo"

    # =========================================================
    # 🔹 Columnas principales
    # =========================================================

    id_servicio_vehiculo = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        index=True
    )

    id_vehiculo = Column(
        Integer,
        ForeignKey("vehiculos.id_vehiculo", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    id_servicio = Column(
        Integer,
        ForeignKey("servicios.id_servicio", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    fecha = Column(Date, nullable=True)
    hora = Column(Time, nullable=True)

    estatus = Column(
        Enum(EstadoSolicitud, name="estado_solicitud_enum"),
        nullable=False,
        server_default=EstadoSolicitud.PROGRAMADA.value
    )

    estatus_servicio_vehiculo = Column(
        Boolean,
        default=True
    )

    # =========================================================
    # 🔹 Auditoría
    # =========================================================

    fecha_registro = Column(
        DateTime(timezone=True),
        server_default=func.now(),  # pylint: disable=not-callable
        nullable=False
    )

    fecha_actualizacion = Column(
        DateTime(timezone=True),
        server_default=func.now(),  # pylint: disable=not-callable
        onupdate=func.now()          # pylint: disable=not-callable
    )

    fecha_servicio = Column(
        DateTime(timezone=True),
        server_default=func.now(),  # pylint: disable=not-callable
        nullable=False
    )

    # =========================================================
    # 🔹 Relaciones
    # =========================================================

    vehiculo = relationship(
        "Vehiculo",
        back_populates="servicios"
    )

    servicio = relationship(
        "Servicio",
        back_populates="vehiculos"
    )

    # =========================================================
    # 🔹 Representación
    # =========================================================

    def __repr__(self) -> str:
        """
        Representación en string del registro de servicio.
        """
        return (
            f"<ServicioVehiculo(id={self.id_servicio_vehiculo}, "
            f"vehiculo_id={self.id_vehiculo}, "
            f"servicio_id={self.id_servicio}, "
            f"estatus='{self.estatus.value}')>"
        )
