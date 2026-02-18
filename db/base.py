"""
Inicialización de la base de datos y registro de modelos.

Este archivo garantiza que todos los modelos estén registrados
antes de ejecutar create_all().
"""

# pylint: disable=unused-import

import logging

from db.session import engine
from models.base import Base

# =========================================================
# 🔹 IMPORTAR TODOS LOS MODELOS (OBLIGATORIO)
# =========================================================

from models.user import User
from models.rols import Rol
from models.cliente import Cliente
from models.vehiculo import Vehiculo
from models.servicio import Servicio
from models.servicio_vehiculo import ServicioVehiculo


# =========================================================
# 🔹 Configuración básica de logging
# =========================================================

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# =========================================================
# 🔹 Crear todas las tablas
# =========================================================

def init_db() -> None:
    """
    Crea todas las tablas definidas en los modelos.
    """

    logger.info("Creando tablas en la base de datos...")
    Base.metadata.create_all(bind=engine)
    logger.info("Tablas creadas correctamente.")


# =========================================================
# 🔹 Eliminar todas las tablas (solo desarrollo)
# =========================================================

def drop_db() -> None:
    """
    Elimina todas las tablas de la base de datos.
    ⚠️ SOLO usar en entorno de desarrollo.
    """

    logger.warning("Eliminando todas las tablas")
    Base.metadata.drop_all(bind=engine)
    logger.warning("Tablas eliminadas correctamente.")


# =========================================================
# 🔹 Ejecutar directamente desde consola
# =========================================================

if __name__ == "__main__":
    init_db()
