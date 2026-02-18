"""
Archivo principal de la aplicación FastAPI.
Registra routers y configura la API.
"""

from fastapi import FastAPI

# Routers
from api.endpoints import (
    rols,
    user,
    cliente,
    vehiculos,
    servicio,
    servicio_vehiculo,
)

from db.base import init_db
init_db()

app = FastAPI(
    title="Autolavado",
    version="1.0.0",
    description="API para gestión de autolavado"
)

# ==============================
# REGISTRO DE RUTAS
# ==============================

app.include_router(rols.router)
app.include_router(user.router)
app.include_router(cliente.router)
app.include_router(vehiculos.router)
app.include_router(servicio.router)
app.include_router(servicio_vehiculo.router)


@app.get("/")
def root():
    """Ruta raíz de prueba."""
    return {"mensaje": "funcionando correctamente"}
