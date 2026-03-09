from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from core.security import get_current_user
from models.user import User

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_current_user)]  # 🔒 BLOQUEA TODO EL ARCHIVO
)

@router.get("/")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()