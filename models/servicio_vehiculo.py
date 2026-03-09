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


class EstadoSolicitud(PyEnum):
    """Posibles estados para una solicitud de servicio."""
    PROGRAMADA = "Programada"
    PROCESO = "Proceso"
    REALIZADA = "Realizada"
    CANCELADA = "Cancelada"


class ServicioVehiculo(Base):
    """
    Registro de servicios aplicados a los vehículos.
    Incluye cajero y operativo que son usuarios del sistema.
    """

    __tablename__ = "servicio_vehiculo"

    # =========================================================
    # Columnas principales
    # =========================================================

    id_servicio_vehiculo = Column(Integer, primary_key=True, autoincrement=True, index=True)

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

    # Usuario que registra la orden (cajero)
    id_cajero = Column(
        Integer,
        ForeignKey("users.id_usuario", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )

    # Usuario que realiza el servicio (operativo)
    id_operativo = Column(
        Integer,
        ForeignKey("users.id_usuario", ondelete="RESTRICT"),
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

    estatus_servicio_vehiculo = Column(Boolean, default=True)

    # =========================================================
    # Auditoría
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
    # Relaciones
    # =========================================================

    vehiculo = relationship("Vehiculo", back_populates="servicios")
    servicio = relationship("Servicio", back_populates="vehiculos")
    cajero   = relationship("User", foreign_keys=[id_cajero])
    operativo = relationship("User", foreign_keys=[id_operativo])

    def __repr__(self) -> str:
        return (
            f"<ServicioVehiculo(id={self.id_servicio_vehiculo}, "
            f"vehiculo_id={self.id_vehiculo}, "
            f"servicio_id={self.id_servicio}, "
            f"cajero_id={self.id_cajero}, "
            f"operativo_id={self.id_operativo}, "
            f"estatus='{self.estatus.value}')>"
        )
        