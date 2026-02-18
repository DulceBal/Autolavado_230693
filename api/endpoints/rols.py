"""
Endpoints de gestión de roles.
Permite crear, consultar, actualizar y eliminar roles del sistema.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.deps import get_db
from schemas.rols import RolCreate, RolRead, RolUpdate
from crud import crud_rol

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post("/", response_model=RolRead)
def create_rol(rol: RolCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo rol en el sistema.
    """
    return crud_rol.create_rol(db, rol)


@router.get("/", response_model=list[RolRead])
def read_roles(db: Session = Depends(get_db)):
    """
    Obtiene la lista de todos los roles registrados.
    """
    return crud_rol.get_roles(db)


@router.get("/{rol_id}", response_model=RolRead)
def read_rol(rol_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un rol específico por su ID.
    """
    db_rol = crud_rol.get_rol(db, rol_id)
    if not db_rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return db_rol


@router.put("/{rol_id}", response_model=RolRead)
def update_rol(rol_id: int, rol: RolUpdate, db: Session = Depends(get_db)):
    """
    Actualiza la información de un rol existente.
    """
    db_rol = crud_rol.update_rol(db, rol_id, rol)
    if not db_rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return db_rol


@router.delete("/{rol_id}")
def delete_rol(rol_id: int, db: Session = Depends(get_db)):
    """
    Elimina un rol del sistema.
    """
    db_rol = crud_rol.delete_rol(db, rol_id)
    if not db_rol:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return {"message": "Rol eliminado correctamente"}
