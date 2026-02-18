"""
Modelo ORM de vehículos.
Representa los vehículos registrados por los clientes.
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
class Vehiculo(Base):
    """
    Representa los vehículos registrados por los clientes.

    Atributos:
        id_vehiculo (int): ID único del vehículo.
        id_cliente (int): FK hacia la tabla clientes.
        marca (str): Marca del vehículo.
        modelo (str): Modelo del vehículo.
        color (str): Color del vehículo.
        placas (str): Número de placa único.
        tipo_vehiculo (str): Tipo de vehículo (auto, camioneta, etc.).
        estatus_vehiculo (bool): Soft delete / activo.
        fecha_creacion (datetime): Fecha de creación del registro.
        fecha_actualizacion (datetime): Fecha de última actualización.
        cliente (Cliente): Relación con la tabla clientes.
        servicios (List[ServicioVehiculo]): Servicios aplicados al vehículo.
    """

    __tablename__ = "vehiculos"

    id_vehiculo = Column(Integer, primary_key=True, index=True)
    id_cliente = Column(
        Integer,
        ForeignKey(
            "clientes.id_cliente",
            ondelete="CASCADE"
        ),
        nullable=False,
        index=True
    )
    marca = Column(String(60), nullable=False, index=True)
    modelo = Column(String(60), nullable=False, index=True)
    color = Column(String(40), nullable=True)
    placas = Column(String(20), nullable=True, unique=True, index=True)
    tipo_vehiculo = Column(String(50), nullable=True)
    estatus_vehiculo = Column(Boolean, default=True)

    fecha_creacion = Column(
        DateTime(timezone=True),
        server_default=func.now(),  # pylint: disable=not-callable
    )
    fecha_actualizacion = Column(
        DateTime(timezone=True),
        server_default=func.now(),  # pylint: disable=not-callable
        onupdate=func.now()          # pylint: disable=not-callable
    )

    cliente = relationship("Cliente", back_populates="vehiculos")
    servicios = relationship(
        "ServicioVehiculo",
        back_populates="vehiculo",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """Representación en string del vehículo."""
        return (
            f"<Vehiculo(id={self.id_vehiculo}, "
            f"marca='{self.marca}', "
            f"modelo='{self.modelo}', "
            f"placas='{self.placas}')>"
        )
