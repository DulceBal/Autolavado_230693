"""
CRUD para historial de servicios aplicados a vehículos.
"""

from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.servicio_vehiculo import ServicioVehiculo
from schemas.servicio_vehiculo import (
    ServicioVehiculoCreate,
    ServicioVehiculoUpdate,
)


# =========================================================
# 🔹 Obtener por ID
# =========================================================

def get_servicio_vehiculo(
    db: Session,
    historial_id: int
) -> ServicioVehiculo:
    """
    Obtiene un servicio del historial por ID.

    Raises:
        HTTPException: 404 si no existe
    """
    historial = (
        db.query(ServicioVehiculo)
        .filter(ServicioVehiculo.id_servicio_vehiculo == historial_id)
        .first()
    )

    if not historial:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Historial con ID {historial_id} no encontrado"
        )

    return historial


# =========================================================
# 🔹 Obtener todos
# =========================================================

def get_servicios_vehiculo(db: Session) -> List[ServicioVehiculo]:
    """Obtiene todos los servicios registrados."""
    return db.query(ServicioVehiculo).all()


# =========================================================
# 🔹 Crear
# =========================================================

def create_servicio_vehiculo(
    db: Session,
    data: ServicioVehiculoCreate
) -> ServicioVehiculo:
    """
    Crea un nuevo registro de servicio.

    Raises:
        HTTPException: 400 si ya existe el mismo registro
    """

    # Evitar duplicados (mismo vehículo + mismo servicio)
    existing = db.query(ServicioVehiculo).filter(
        ServicioVehiculo.id_vehiculo == data.id_vehiculo,
        ServicioVehiculo.id_servicio == data.id_servicio
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este servicio ya está registrado para el vehículo"
        )

    nuevo = ServicioVehiculo(**data.model_dump())

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return nuevo


# =========================================================
# 🔹 Actualizar
# =========================================================

def update_servicio_vehiculo(
    db: Session,
    historial_id: int,
    data: ServicioVehiculoUpdate
) -> ServicioVehiculo:
    """
    Actualiza un servicio del historial.

    Raises:
        HTTPException: 404 si no existe
    """
    historial = get_servicio_vehiculo(db, historial_id)

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(historial, key, value)

    db.commit()
    db.refresh(historial)

    return historial


# =========================================================
# 🔹 Eliminar
# =========================================================

def delete_servicio_vehiculo(
    db: Session,
    historial_id: int
) -> bool:
    """
    Elimina un servicio del historial.

    Raises:
        HTTPException: 404 si no existe
    """
    historial = get_servicio_vehiculo(db, historial_id)

    db.delete(historial)
    db.commit()

    return True
