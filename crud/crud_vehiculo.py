"""
Operaciones CRUD para vehículos.
"""

from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.vehiculo import Vehiculo
from schemas.vehiculo import VehiculoCreate, VehiculoUpdate


# =========================================================
# 🔹 Obtener vehículo por ID
# =========================================================

def get_vehiculo(db: Session, vehiculo_id: int) -> Vehiculo:
    """
    Obtiene un vehículo por su ID.

    Raises:
        HTTPException: 404 si no existe
    """
    vehiculo = db.query(Vehiculo).filter(
        Vehiculo.id_vehiculo == vehiculo_id
    ).first()

    if not vehiculo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vehículo con ID {vehiculo_id} no encontrado"
        )

    return vehiculo


# =========================================================
# 🔹 Obtener lista de vehículos
# =========================================================

def get_vehiculos(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[Vehiculo]:
    """Obtiene una lista paginada de vehículos."""
    return db.query(Vehiculo).offset(skip).limit(limit).all()


# =========================================================
# 🔹 Crear vehículo
# =========================================================

def create_vehiculo(
    db: Session,
    vehiculo_in: VehiculoCreate
) -> Vehiculo:
    """
    Crea un nuevo vehículo.

    Raises:
        HTTPException: 400 si ya existe (por ejemplo, misma placa)
    """

    # Validación opcional si tu modelo tiene campo placa único
    if hasattr(Vehiculo, "placa"):
        existing = db.query(Vehiculo).filter(
            Vehiculo.placa == vehiculo_in.placa
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El vehículo con placa '{vehiculo_in.placa}' ya existe"
            )

    db_vehiculo = Vehiculo(**vehiculo_in.model_dump())

    db.add(db_vehiculo)
    db.commit()
    db.refresh(db_vehiculo)

    return db_vehiculo


# =========================================================
# 🔹 Actualizar vehículo
# =========================================================

def update_vehiculo(
    db: Session,
    vehiculo_id: int,
    vehiculo_update: VehiculoUpdate
) -> Vehiculo:
    """
    Actualiza un vehículo existente.

    Raises:
        HTTPException: 404 si no existe
        HTTPException: 400 si intenta duplicar placa
    """

    db_vehiculo = get_vehiculo(db, vehiculo_id)

    update_data = vehiculo_update.model_dump(exclude_unset=True)

    # Validación opcional si actualiza placa
    if "placa" in update_data:
        existing = db.query(Vehiculo).filter(
            Vehiculo.placa == update_data["placa"],
            Vehiculo.id_vehiculo != vehiculo_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El vehículo con placa '{update_data['placa']}' ya existe"
            )

    for key, value in update_data.items():
        setattr(db_vehiculo, key, value)

    db.commit()
    db.refresh(db_vehiculo)

    return db_vehiculo


# =========================================================
# 🔹 Eliminar vehículo
# =========================================================

def delete_vehiculo(
    db: Session,
    vehiculo_id: int
) -> bool:
    """
    Elimina un vehículo por ID.

    Raises:
        HTTPException: 404 si no existe
    """

    db_vehiculo = get_vehiculo(db, vehiculo_id)

    db.delete(db_vehiculo)
    db.commit()

    return True
