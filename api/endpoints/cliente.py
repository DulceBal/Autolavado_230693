"""
Endpoints de clientes.
Permite crear, consultar, actualizar y eliminar clientes.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.deps import get_db
from schemas.cliente import ClienteCreate, ClienteRead, ClienteUpdate
from crud import crud_cliente as crud

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.post("/", response_model=ClienteRead)
def create_cliente(cliente: ClienteCreate, db: Session = Depends(get_db)):
    """Crear un nuevo cliente."""
    return crud.create_cliente(db, cliente)


@router.get("/", response_model=list[ClienteRead])
def read_clientes(db: Session = Depends(get_db)):
    """Obtener todos los clientes."""
    return crud.get_clientes(db)


@router.get("/{cliente_id}", response_model=ClienteRead)
def read_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Obtener un cliente por ID."""
    return crud.get_cliente(db, cliente_id)


@router.put("/{cliente_id}", response_model=ClienteRead)
def update_cliente(
    cliente_id: int,
    cliente: ClienteUpdate,
    db: Session = Depends(get_db),
):
    """Actualizar un cliente existente."""
    return crud.update_cliente(db, cliente_id, cliente)


@router.delete("/{cliente_id}")
def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    """Eliminar un cliente."""
    return crud.delete_cliente(db, cliente_id)
