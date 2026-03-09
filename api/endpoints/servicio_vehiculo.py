"""
Endpoints para el historial de servicios aplicados a vehículos.
Permite registrar, consultar, actualizar y eliminar servicios realizados.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.deps import get_db
from schemas.servicio_vehiculo import (
    ServicioVehiculoCreate,
    ServicioVehiculoRead,
)
from crud import crud_servicio_vehiculo as crud_sv

router = APIRouter(prefix="/Servicio_vehiculo", tags=["Servicio_vehiculo"])


@router.post("/", response_model=ServicioVehiculoRead)
def create_historial(data: ServicioVehiculoCreate, db: Session = Depends(get_db)):
    """Registra un nuevo servicio aplicado a un vehículo."""
    return crud_sv.create_servicio_vehiculo(db, data)


@router.get("/", response_model=list[ServicioVehiculoRead])
def read_historial(db: Session = Depends(get_db)):
    """Obtiene todo el historial de servicios realizados."""
    return crud_sv.get_servicios_vehiculo(db)


@router.get("/{historial_id}", response_model=ServicioVehiculoRead)
def read_historial_by_id(historial_id: int, db: Session = Depends(get_db)):
    """Obtiene un servicio específico por su ID."""
    historial = crud_sv.get_servicio_vehiculo(db, historial_id)
    if not historial:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return historial


@router.put("/{historial_id}", response_model=ServicioVehiculoRead)
def update_historial(historial_id: int, data: ServicioVehiculoCreate, db: Session = Depends(get_db)):
    """Actualiza la información de un servicio registrado."""
    historial = crud_sv.update_servicio_vehiculo(db, historial_id, data)
    if not historial:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return historial


@router.delete("/{historial_id}")
def delete_historial(historial_id: int, db: Session = Depends(get_db)):
    """Elimina un registro del historial de servicios."""
    historial = crud_sv.delete_servicio_vehiculo(db, historial_id)
    if not historial:
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return {"message": "Servicio eliminado correctamente"}
