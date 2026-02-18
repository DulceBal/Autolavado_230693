"""
Dependencias reutilizables para la API.
Centraliza las dependencias que pueden ser compartidas
entre múltiples endpoints.
"""

from typing import Generator
from sqlalchemy.orm import Session

from db.session import get_db as _get_db


def get_db() -> Generator[Session, None, None]:
    """
    Dependency que proporciona una sesión de base de datos
    por cada petición y la cierra automáticamente.
    """
    yield from _get_db()


__all__ = ["get_db"]
