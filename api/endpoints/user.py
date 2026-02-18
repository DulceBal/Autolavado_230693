"""
Rutas API para usuarios.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.deps import get_db
from schemas.user import UserCreate, UserRead, UserUpdate
from crud import crud_user

router = APIRouter(prefix="/users", tags=["Usuarios"])


# =============================
# CREAR USUARIO
# =============================
@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Crear un nuevo usuario."""
    return crud_user.create_user(db, user)


# =============================
# LISTAR USUARIOS
# =============================
@router.get("/", response_model=list[UserRead])
def read_users(db: Session = Depends(get_db)):
    """Obtener todos los usuarios."""
    return crud_user.get_users(db)


# =============================
# OBTENER USUARIO POR ID
# =============================
@router.get("/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """Obtener un usuario específico."""
    db_user = crud_user.get_user(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user


# =============================
# ACTUALIZAR USUARIO
# =============================
@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """Actualizar un usuario."""
    db_user = crud_user.update_user(db, user_id, user)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_user


# =============================
# ELIMINAR USUARIO
# =============================
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Eliminar un usuario."""
    success = crud_user.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"message": "Usuario eliminado correctamente"}
