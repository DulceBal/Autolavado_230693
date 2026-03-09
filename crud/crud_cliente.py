from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.cliente import Cliente
from schemas.cliente import ClienteCreate, ClienteUpdate


# Obtener cliente por ID
def get_cliente(db: Session, cliente_id: int) -> Cliente:
    cliente = db.query(Cliente).filter(
        Cliente.id_cliente == cliente_id
    ).first()

    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cliente con ID {cliente_id} no encontrado"
        )

    return cliente


# Listar clientes
def get_clientes(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> List[Cliente]:
    return db.query(Cliente).offset(skip).limit(limit).all()


# Crear cliente
def create_cliente(db: Session, cliente_in: ClienteCreate) -> Cliente:
    db_cliente = Cliente(**cliente_in.model_dump())

    db.add(db_cliente)
    db.commit()
    db.refresh(db_cliente)

    return db_cliente


# Actualizar cliente
def update_cliente(
    db: Session,
    cliente_id: int,
    cliente_update: ClienteUpdate,
) -> Cliente:

    db_cliente = get_cliente(db, cliente_id)

    update_data = cliente_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_cliente, key, value)

    db.commit()
    db.refresh(db_cliente)

    return db_cliente


# Eliminar cliente
def delete_cliente(db: Session, cliente_id: int) -> bool:
    db_cliente = get_cliente(db, cliente_id)

    db.delete(db_cliente)
    db.commit()

    return True
    