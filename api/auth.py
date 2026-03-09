from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from models.user import User
from schemas.user import UserLogin
from passlib.context import CryptContext
from core.security import create_access_token

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.correo_usuario == form_data.username
    ).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Usuario no existe")

    if not verify_password(form_data.password, db_user.password_usuario):
        raise HTTPException(status_code=401, detail="Contraseña incorrecta")

    access_token = create_access_token(
        data={"sub": db_user.correo_usuario}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }