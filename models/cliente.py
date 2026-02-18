"""
Modelo ORM de clientes.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from models.base import Base


# pylint: disable=too-few-public-methods
class Cliente(Base):
    """
    Representa los clientes del autolavado.

    Atributos:
        id_cliente (int): ID único del cliente.
        nombre_cliente (str): Nombre completo del cliente.
        telefono_cliente (str | None): Teléfono del cliente.
        email_cliente (str | None): Correo electrónico del cliente.
        estatus_cliente (bool): Estado activo/inactivo.
        fecha_creacion (datetime): Fecha de creación del registro.
        fecha_actualizacion (datetime): Fecha de última actualización.
        vehiculos (List[Vehiculo]): Vehículos asociados al cliente.
    """

    __tablename__ = "clientes"

    # =========================================================
    # 🔹 Columnas
    # =========================================================

    id_cliente = Column(Integer, primary_key=True, index=True)

    nombre_cliente = Column(
        String(120),
        nullable=False,
        index=True
    )

    telefono_cliente = Column(
        String(20),
        nullable=True
    )

    email_cliente = Column(
        String(120),
        nullable=True,
        unique=True,  # recomendable si usas email como identificador
        index=True
    )

    estatus_cliente = Column(
        Boolean,
        default=True
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

    # Un cliente puede tener varios vehículos
    vehiculos = relationship(
        "Vehiculo",
        back_populates="cliente",
        cascade="all, delete-orphan"
    )

    # =========================================================
    # 🔹 Representación
    # =========================================================

    def __repr__(self) -> str:
        """
        Representación en string del cliente.
        """
        return (
            f"<Cliente(id={self.id_cliente}, "
            f"nombre='{self.nombre_cliente}', "
            f"email='{self.email_cliente}')>"
        )
