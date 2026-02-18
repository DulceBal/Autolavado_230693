"""Endpoints para la gestión de vehículos."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.deps import get_db
from schemas.vehiculo import VehiculoCreate, VehiculoRead
from crud import crud_vehiculo

router = APIRouter(prefix="/vehiculos", tags=["Vehiculos"])


@router.post("/", response_model=VehiculoRead)
def create_vehiculo(data: VehiculoCreate, db: Session = Depends(get_db)):
    """Registra un nuevo vehículo."""
    return crud_vehiculo.create_vehiculo(db, data)


@router.get("/", response_model=list[VehiculoRead])
def get_vehiculos(db: Session = Depends(get_db)):
    """Obtiene todos los vehículos registrados."""
    return crud_vehiculo.get_vehiculos(db)


@router.get("/{vehiculo_id}", response_model=VehiculoRead)
def get_vehiculo(vehiculo_id: int, db: Session = Depends(get_db)):
    """Obtiene un vehículo específico por su ID."""
    vehiculo = crud_vehiculo.get_vehiculo(db, vehiculo_id)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehiculo


@router.put("/{vehiculo_id}", response_model=VehiculoRead)
def update_vehiculo(vehiculo_id: int, data: VehiculoCreate, db: Session = Depends(get_db)):
    """Actualiza la información de un vehículo registrado."""
    vehiculo = crud_vehiculo.update_vehiculo(db, vehiculo_id, data)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return vehiculo


@router.delete("/{vehiculo_id}")
def delete_vehiculo(vehiculo_id: int, db: Session = Depends(get_db)):
    """Elimina un vehículo registrado."""
    vehiculo = crud_vehiculo.delete_vehiculo(db, vehiculo_id)
    if not vehiculo:
        raise HTTPException(status_code=404, detail="Vehículo no encontrado")
    return {"mensaje": "Vehículo eliminado"}
