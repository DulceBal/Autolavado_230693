"""
Modelo ORM de productos.
"""

from sqlalchemy import (
    Column,
    Integer,
    String,
    Numeric,
    Boolean,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship

from models.base import Base


class Producto(Base):
    __tablename__ = "productos"

    id_producto = Column(Integer, primary_key=True, autoincrement=True, index=True)
    nombre_producto = Column(String(150), nullable=False, index=True)
    descripcion_producto = Column(String(300), nullable=True)
    precio = Column(Numeric(10, 2), nullable=False)
    descuento_porcentaje = Column(Numeric(5, 2), nullable=False, default=0.00)
    stock = Column(Integer, nullable=False, default=0)
    unidad_medida = Column(String(50), nullable=False, default="pieza")
    estatus_producto = Column(Boolean, default=True)
    precio_final = Column(Numeric(10, 2), nullable=False)

    id_servicio = Column(
        Integer,
        ForeignKey("servicios.id_servicio", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    fecha_creacion = Column(DateTime(timezone=False), server_default=func.now())
    fecha_actualizacion = Column(
        DateTime(timezone=False),
        server_default=func.now(),
        onupdate=func.now(),
    )

    servicio = relationship("Servicio", back_populates="productos")

    def __repr__(self) -> str:
        return (
            f"<Producto(id_producto={self.id_producto}, "
            f"nombre='{self.nombre_producto}', "
            f"precio_final={self.precio_final})>"
        )