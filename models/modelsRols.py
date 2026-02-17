'''
Docstring for models.rols
Este archivo define el modelo de datos para los roles de usuario en la aplicación.
Utiliza SQLAlchemy para mapear la clase Rols a la tabla 'rols' en la base de datos. Cada rol tiene un ID único y un nombre asociado.
'''
from sqlalchemy import Column, Integer, String, Boolean
from config.db import Base

class Rols(Base):
    '''
    Modelo de datos para los roles de usuario.
    Atributos:
        id_rol (Integer): Identificador único del rol.
        nombre_rol (String): Nombre del rol.
    '''
    __tablename__ = 'tbc_rols'
    id_rol = Column(Integer, primary_key=True, index=True , autoincrement=True)
    descripcion_rol = Column(String(100), unique=True, index=True, nullable=False)
    nombre_rol = Column(String(50), unique=True, index=True, nullable=False)
    estatus_rol = Column(Boolean, default=True, nullable=False)
    def __repr__(self):
        return f"<Rols(id_rol={self.id_rol}, nombre_rol='{self.nombre_rol}', descripcion_rol='{self.descripcion_rol}', estatus_rol={self.estatus_rol})>"
    def to_dict(self):
        return {
            "id_rol": self.id_rol,
            "nombre_rol": self.nombre_rol,
            "descripcion_rol": self.descripcion_rol,
            "estatus_rol": self.estatus_rol
        }
    def from_dict(self, data):
        for field in ['nombre_rol', 'descripcion_rol', 'estatus_rol']:
            if field in data:
                setattr(self, field, data[field])
    def __init__(self, nombre_rol: str, descripcion_rol: str, estatus_rol: bool = True):
        self.nombre_rol = nombre_rol
        self.descripcion_rol = descripcion_rol
        self.estatus_rol = estatus_rol
    pass
# Fin del archivo models/modelsRols.py
