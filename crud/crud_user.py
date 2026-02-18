"""
Operaciones CRUD para usuarios.
"""

from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.user import User
from schemas.user import UserCreate, UserUpdate
from core.security import get_password_hash


# =========================================================
# 🔹 CREATE
# =========================================================

def create_user(db: Session, user: UserCreate) -> User:
    """
    Crea un nuevo usuario.

    Args:
        db (Session): Sesión de base de datos.
        user (UserCreate): Datos del usuario a crear.

    Raises:
        HTTPException: 400 si el correo o nombre ya existen.

    Returns:
        User: Usuario creado.
    """

    # Validar email duplicado
    if db.query(User).filter(User.correo_usuario == user.correo_usuario).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya está registrado"
        )

    # Validar nombre duplicado
    if db.query(User).filter(User.nombre_usuario == user.nombre_usuario).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya existe"
        )

    hashed_password = get_password_hash(user.password_usuario)

    db_user = User(
        nombre_usuario=user.nombre_usuario,
        correo_usuario=user.correo_usuario,
        password_usuario=hashed_password,
        id_rol=user.id_rol,
        activo=True
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# =========================================================
# 🔹 READ
# =========================================================

def get_user(db: Session, user_id: int) -> User:
    """
    Obtiene un usuario por ID.

    Raises:
        HTTPException: 404 si no existe.
    """
    user = db.query(User).filter(User.id_usuario == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado"
        )
    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Obtiene un usuario por correo electrónico.
    """
    return db.query(User).filter(User.correo_usuario == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """
    Lista usuarios activos.
    """
    return (
        db.query(User)
        .filter(User.activo.is_(True))
        .offset(skip)
        .limit(limit)
        .all()
    )


# =========================================================
# 🔹 UPDATE
# =========================================================

def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User:
    """
    Actualiza los datos de un usuario.

    Raises:
        HTTPException: 404 si el usuario no existe.
        HTTPException: 400 si intenta duplicar email o nombre.
    """
    db_user = get_user(db, user_id)

    update_data = user_data.model_dump(exclude_unset=True)  # Pydantic v2
    # Si usas Pydantic <2, reemplaza por: user_data.dict(exclude_unset=True)

    # Validar duplicado email
    if "correo_usuario" in update_data:
        if db.query(User).filter(
            User.correo_usuario == update_data["correo_usuario"],
            User.id_usuario != user_id
        ).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El correo ya está registrado"
            )

    # Validar duplicado username
    if "nombre_usuario" in update_data:
        if db.query(User).filter(
            User.nombre_usuario == update_data["nombre_usuario"],
            User.id_usuario != user_id
        ).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nombre de usuario ya existe"
            )

    # Hashear contraseña si se actualiza
    if "password_usuario" in update_data:
        update_data["password_usuario"] = get_password_hash(update_data["password_usuario"])

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return db_user


# =========================================================
# 🔹 DELETE (Soft Delete)
# =========================================================

def delete_user(db: Session, user_id: int) -> User:
    """
    Desactiva un usuario (eliminación lógica).

    Raises:
        HTTPException: 404 si no existe.
    """
    db_user = get_user(db, user_id)

    db_user.activo = False

    db.commit()
    db.refresh(db_user)

    return db_user
