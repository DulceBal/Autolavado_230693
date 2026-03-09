"""
CRUD para historial de servicios aplicados a vehículos.
Cajero  = rol 3
Operativo = rol 4
"""

from typing import List, Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from models.servicio_vehiculo import ServicioVehiculo
from models.user import User
from models.vehiculo import Vehiculo
from models.servicio import Servicio
from schemas.servicio_vehiculo import (
    ServicioVehiculoCreate,
    ServicioVehiculoUpdate,
)

# IDs de rol fijos
ROL_CAJERO    = 3
ROL_OPERATIVO = 4


def _with_relations(query):
    return query.options(
        joinedload(ServicioVehiculo.vehiculo),
        joinedload(ServicioVehiculo.servicio),
        joinedload(ServicioVehiculo.cajero),
        joinedload(ServicioVehiculo.operativo),
    )


def _resolver_usuario(
    db: Session,
    id_usuario: Optional[int],
    nombre_usuario: Optional[str],
    id_rol_requerido: int,
    nombre_rol: str,
) -> User:
    """
    Busca un usuario por ID, nombre o ambos, y valida que tenga el rol correcto.
    """
    if not id_usuario and not nombre_usuario:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{nombre_rol}: debes proporcionar id_{nombre_rol.lower()} o nombre_{nombre_rol.lower()}"
        )

    # Buscar usuario
    if id_usuario and nombre_usuario:
        user = db.query(User).filter(User.id_usuario == id_usuario).first()
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                detail=f"{nombre_rol}: usuario con id {id_usuario} no encontrado")
        if user.nombre_usuario != nombre_usuario:
            raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                detail=f"{nombre_rol}: el id {id_usuario} pertenece a '{user.nombre_usuario}', no a '{nombre_usuario}'")
    elif id_usuario:
        user = db.query(User).filter(User.id_usuario == id_usuario).first()
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                detail=f"{nombre_rol}: usuario con id {id_usuario} no encontrado")
    else:
        user = db.query(User).filter(User.nombre_usuario == nombre_usuario).first()
        if not user:
            raise HTTPException(status.HTTP_404_NOT_FOUND,
                                detail=f"{nombre_rol}: usuario con nombre '{nombre_usuario}' no encontrado")

    # Validar que tenga el rol correcto
    if user.id_rol != id_rol_requerido:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail=f"'{user.nombre_usuario}' no tiene el rol de {nombre_rol} (rol {id_rol_requerido}). "
                   f"Su rol actual es {user.id_rol}. Asigna el rol correcto al usuario primero."
        )

    return user


# =========================================================
# GET por ID
# =========================================================

def get_servicio_vehiculo(db: Session, historial_id: int) -> ServicioVehiculo:
    historial = (
        _with_relations(db.query(ServicioVehiculo))
        .filter(ServicioVehiculo.id_servicio_vehiculo == historial_id)
        .first()
    )
    if not historial:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Historial con ID {historial_id} no encontrado")
    return historial


# =========================================================
# GET todos
# =========================================================

def get_servicios_vehiculo(db: Session) -> List[ServicioVehiculo]:
    return _with_relations(db.query(ServicioVehiculo)).all()


# =========================================================
# POST
# =========================================================

def create_servicio_vehiculo(db: Session, data: ServicioVehiculoCreate) -> ServicioVehiculo:
    # Validar vehículo y servicio
    if not db.query(Vehiculo).filter(Vehiculo.id_vehiculo == data.id_vehiculo).first():
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Vehículo con id {data.id_vehiculo} no encontrado")
    if not db.query(Servicio).filter(Servicio.id_servicio == data.id_servicio).first():
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"Servicio con id {data.id_servicio} no encontrado")

    # Resolver cajero (rol 3) y operativo (rol 4)
    cajero    = _resolver_usuario(db, data.id_cajero, data.nombre_cajero, ROL_CAJERO, "Cajero")
    operativo = _resolver_usuario(db, data.id_operativo, data.nombre_operativo, ROL_OPERATIVO, "Operativo")

    nuevo = ServicioVehiculo(
        id_vehiculo=data.id_vehiculo,
        id_servicio=data.id_servicio,
        id_cajero=cajero.id_usuario,
        id_operativo=operativo.id_usuario,
        fecha=data.fecha,
        hora=data.hora,
        estatus=data.estatus,
    )

    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)

    return get_servicio_vehiculo(db, nuevo.id_servicio_vehiculo)


# =========================================================
# PUT
# =========================================================

def update_servicio_vehiculo(db: Session, historial_id: int, data: ServicioVehiculoUpdate) -> ServicioVehiculo:
    historial = get_servicio_vehiculo(db, historial_id)

    if data.id_cajero or data.nombre_cajero:
        cajero = _resolver_usuario(db, data.id_cajero, data.nombre_cajero, ROL_CAJERO, "Cajero")
        historial.id_cajero = cajero.id_usuario

    if data.id_operativo or data.nombre_operativo:
        operativo = _resolver_usuario(db, data.id_operativo, data.nombre_operativo, ROL_OPERATIVO, "Operativo")
        historial.id_operativo = operativo.id_usuario

    campos_simples = data.model_dump(
        exclude_unset=True,
        exclude={"id_cajero", "nombre_cajero", "id_operativo", "nombre_operativo"}
    )
    for key, value in campos_simples.items():
        setattr(historial, key, value)

    db.commit()
    db.refresh(historial)

    return get_servicio_vehiculo(db, historial_id)


# =========================================================
# DELETE
# =========================================================

def delete_servicio_vehiculo(db: Session, historial_id: int) -> bool:
    historial = get_servicio_vehiculo(db, historial_id)
    db.delete(historial)
    db.commit()
    return True