"""
Módulo de endpoints de servicio.

Aquí se definen las rutas y lógica relacionadas con los servicios de vehículos,
incluyendo creación, lectura, actualización y eliminación.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.deps import get_db
from schemas.servicio import ServicioCreate, ServicioRead
from crud import crud_servicio

router = APIRouter(prefix="/servicios", tags=["Servicios"])


@router.post("/", response_model=ServicioRead)
def create_servicio(data: ServicioCreate, db: Session = Depends(get_db)):
    """
    Crea un nuevo servicio de vehículo.
    """
    return crud_servicio.create_servicio(db, data)


@router.get("/", response_model=list[ServicioRead])
def get_servicios(db: Session = Depends(get_db)):
    """
    Obtiene todos los servicios de vehículos.
    """
    return crud_servicio.get_servicios(db)


@router.get("/{servicio_id}", response_model=ServicioRead)
def get_servicio(servicio_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un servicio de vehículo por su ID.
    """
    servicio = crud_servicio.get_servicio(db, servicio_id)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio


@router.put("/{servicio_id}", response_model=ServicioRead)
def update_servicio(servicio_id: int, data: ServicioCreate, db: Session = Depends(get_db)):
    """
    Actualiza un servicio de vehículo existente.
    """
    servicio = crud_servicio.update_servicio(db, servicio_id, data)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return servicio


@router.delete("/{servicio_id}")
def delete_servicio(servicio_id: int, db: Session = Depends(get_db)):
    """
    Elimina un servicio de vehículo por su ID.
    """
    servicio = crud_servicio.delete_servicio(db, servicio_id)
    if not servicio:
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    return {"mensaje": "Servicio eliminado"}
