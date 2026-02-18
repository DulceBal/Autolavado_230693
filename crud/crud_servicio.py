"""
Operaciones CRUD para el modelo Servicio.
"""

from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.servicio import Servicio
from schemas.servicio import ServicioCreate, ServicioUpdate


# =========================================================
# 🔹 Obtener servicio por ID
# =========================================================

def get_servicio(db: Session, servicio_id: int) -> Servicio:
    """
    Obtiene un servicio por su ID.

    Raises:
        HTTPException: 404 si no existe
    """
    servicio = (
        db.query(Servicio)
        .filter(Servicio.id_servicio == servicio_id)
        .first()
    )

    if not servicio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Servicio con ID {servicio_id} no encontrado"
        )

    return servicio


# =========================================================
# 🔹 Obtener lista de servicios
# =========================================================

def get_servicios(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[Servicio]:
    """Obtiene una lista paginada de servicios."""
    return db.query(Servicio).offset(skip).limit(limit).all()


# =========================================================
# 🔹 Crear servicio
# =========================================================

def create_servicio(
    db: Session,
    servicio_in: ServicioCreate
) -> Servicio:
    """
    Crea un nuevo servicio.

    Raises:
        HTTPException: 400 si ya existe (por ejemplo, mismo nombre)
    """

    # Validación opcional de duplicado por nombre
    if hasattr(Servicio, "nombre_servicio"):
        existing = db.query(Servicio).filter(
            Servicio.nombre_servicio == servicio_in.nombre_servicio
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El servicio '{servicio_in.nombre_servicio}' ya existe"
            )

    db_servicio = Servicio(**servicio_in.model_dump())

    db.add(db_servicio)
    db.commit()
    db.refresh(db_servicio)

    return db_servicio


# =========================================================
# 🔹 Actualizar servicio
# =========================================================

def update_servicio(
    db: Session,
    servicio_id: int,
    servicio_update: ServicioUpdate
) -> Servicio:
    """
    Actualiza un servicio existente.

    Raises:
        HTTPException: 404 si no existe
        HTTPException: 400 si intenta duplicar nombre
    """
    db_servicio = get_servicio(db, servicio_id)

    update_data = servicio_update.model_dump(exclude_unset=True)

    # Validación opcional de duplicado si se actualiza nombre
    if "nombre_servicio" in update_data:
        existing = db.query(Servicio).filter(
            Servicio.nombre_servicio == update_data["nombre_servicio"],
            Servicio.id_servicio != servicio_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El servicio '{update_data['nombre_servicio']}' ya existe"
            )

    for key, value in update_data.items():
        setattr(db_servicio, key, value)

    db.commit()
    db.refresh(db_servicio)

    return db_servicio


# =========================================================
# 🔹 Eliminar servicio
# =========================================================

def delete_servicio(
    db: Session,
    servicio_id: int
) -> bool:
    """
    Elimina un servicio por ID.

    Raises:
        HTTPException: 404 si no existe
    """
    db_servicio = get_servicio(db, servicio_id)

    db.delete(db_servicio)
    db.commit()

    return True
