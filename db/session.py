"""
Configuración de la conexión y sesiones de base de datos con SQLAlchemy.
Versión síncrona (recomendada si no usas async en tus endpoints).
"""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

from core.config import settings


# =========================================================
# 🔹 ENGINE (Motor de Base de Datos)
# =========================================================

engine = create_engine(
    settings.DATABASE_URL,   # Construida en config.py
    echo=settings.DB_ECHO,   # Mostrar queries SQL en consola (solo desarrollo)
    pool_pre_ping=True,      # Verifica conexión antes de usarla
    pool_size=5,             # Conexiones persistentes
    max_overflow=10,         # Conexiones adicionales temporales
    pool_timeout=30,         # Tiempo máximo de espera
    future=True              # Estilo SQLAlchemy 2.x
)


# =========================================================
# 🔹 SESSION LOCAL
# =========================================================

SessionLocal = sessionmaker(  # pylint: disable=invalid-name
    autocommit=False,
    autoflush=False,
    bind=engine,
    expire_on_commit=False,
    class_=Session
)


# =========================================================
# 🔹 BASE DECLARATIVA
# =========================================================

class Base(DeclarativeBase):  # pylint: disable=too-few-public-methods
    """
    Clase base para todos los modelos ORM.
    Todos los modelos deben heredar de Base.
    """
    # No es necesario el pass, el docstring basta


# =========================================================
# 🔹 DEPENDENCY PARA FASTAPI
# =========================================================

def get_db() -> Generator[Session, None, None]:
    """
    Proporciona una sesión de base de datos.
    Se usa como dependency en los endpoints:

        def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db: Session = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
