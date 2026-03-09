"""
Archivo principal de la aplicación FastAPI.
Registra routers y configura la API.
"""

from fastapi import FastAPI
from api import auth
from core.security import get_current_user
from fastapi import Depends
from db.base import init_db
from db.base import Base   

app = FastAPI()
# ==============================
# CREAR APP PRIMERO
# ==============================

app = FastAPI(
    title="Autolavado",
    version="1.0.0",
    description="API para gestión de autolavado"
)

# ==============================
# BASE DE DATOS
# ==============================


init_db()
print(Base.metadata.tables.keys())

# ==============================
# IMPORTAR ROUTERS
# ==============================

from api.endpoints import (
    rols,
    user,
    cliente,
    vehiculos,
    servicio,
    servicio_vehiculo,
    producto,
)

# ==============================
# REGISTRO DE RUTAS
# ==============================

app.include_router(auth.router, prefix="/auth", tags=["Auth"])

# RUTAS PROTEGIDAS
app.include_router(rols.router, dependencies=[Depends(get_current_user)])
app.include_router(user.router, dependencies=[Depends(get_current_user)])
app.include_router(cliente.router, dependencies=[Depends(get_current_user)])
app.include_router(vehiculos.router, dependencies=[Depends(get_current_user)])
app.include_router(servicio.router, dependencies=[Depends(get_current_user)])
app.include_router(servicio_vehiculo.router, dependencies=[Depends(get_current_user)])
app.include_router(producto.router, dependencies=[Depends(get_current_user)])

@app.get("/")
def root():
    return {"mensaje": "API Autolavado funcionando correctamente"}