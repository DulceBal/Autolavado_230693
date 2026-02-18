"""
Operaciones CRUD para el modelo Rol.
"""

from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.rols import Rol
from schemas.rols import RolCreate, RolUpdate


# =========================================================
# 🔹 Obtener un rol por ID
# =========================================================

def get_rol(db: Session, rol_id: int) -> Rol:
    """
    Obtiene un rol por su ID.

    Raises:
        HTTPException: 404 si el rol no existe
    """
    rol = db.query(Rol).filter(Rol.id_rol == rol_id).first()

    if not rol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Rol con ID {rol_id} no encontrado"
        )

    return rol


# =========================================================
# 🔹 Obtener lista de roles (con búsqueda opcional)
# =========================================================

def get_roles(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    search: Optional[str] = None,
) -> List[Rol]:
    """
    Obtiene una lista paginada de roles.
    Permite búsqueda opcional por nombre.
    """
    query = db.query(Rol)

    if search:
        query = query.filter(Rol.nombre_rol.ilike(f"%{search}%"))

    return query.offset(skip).limit(limit).all()


# =========================================================
# 🔹 Crear rol
# =========================================================

def create_rol(db: Session, rol_in: RolCreate) -> Rol:
    """
    Crea un nuevo rol.

    Raises:
        HTTPException: 400 si ya existe
    """
    existing = db.query(Rol).filter(
        Rol.nombre_rol == rol_in.nombre_rol
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El rol '{rol_in.nombre_rol}' ya existe"
        )

    db_rol = Rol(**rol_in.model_dump())

    db.add(db_rol)
    db.commit()
    db.refresh(db_rol)

    return db_rol


# =========================================================
# 🔹 Actualizar rol
# =========================================================

def update_rol(
    db: Session,
    rol_id: int,
    rol_update: RolUpdate,
) -> Rol:
    """
    Actualiza un rol existente (solo campos enviados).

    Raises:
        HTTPException: 404 si no existe
        HTTPException: 400 si intenta duplicar nombre
    """
    db_rol = get_rol(db, rol_id)

    update_data = rol_update.model_dump(exclude_unset=True)

    # Validar duplicado si se actualiza nombre
    if "nombre_rol" in update_data:
        existing = db.query(Rol).filter(
            Rol.nombre_rol == update_data["nombre_rol"],
            Rol.id_rol != rol_id
        ).first()

        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El rol '{update_data['nombre_rol']}' ya existe"
            )

    for key, value in update_data.items():
        setattr(db_rol, key, value)

    db.commit()
    db.refresh(db_rol)

    return db_rol


# =========================================================
# 🔹 Eliminar rol
# =========================================================

def delete_rol(db: Session, rol_id: int) -> bool:
    """
    Elimina un rol por ID.

    Raises:
        HTTPException: 404 si no existe
    """
    db_rol = get_rol(db, rol_id)

    db.delete(db_rol)
    db.commit()

    return True
