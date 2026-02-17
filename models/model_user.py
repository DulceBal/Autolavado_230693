'''
Docstring for models.modelUser
Este archivo define el modelo de datos para los usuarios en la aplicación.
Utiliza SQLAlchemy para mapear la clase User a la tabla 'users' en la base
de datos. Cada usuario tiene un ID único, nombre, correo electrónico y una referencia al rol que posee.
'''
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Date
from sqlalchemy.orm import relationship
from config.db import Base

class User(Base): 
    '''
    Modelo de datos para los usuarios.
    Atributos:
        id_user (Integer): Identificador único del usuario.
        nombre_user (String): Nombre del usuario.
        email_user (String): Correo electrónico del usuario.
        rol_id (Integer): Identificador del rol asociado al usuario.
    '''
    __tablename__ = 'tbb_users'
    id_user = Column(Integer, primary_key=True, index=True , autoincrement=True)
    nombre_user = Column(String(100), unique=True, index=True, nullable=False)
    apellido_user = Column(String(100), unique=False, index=True, nullable=False)
    telefono_user = Column(String(15), unique=False, index=True, nullable=True)
    email_user = Column(String(100), unique=True, index=True, nullable=False)
    password_user = Column(String(100), nullable=False)
    rol_id = Column(Integer, ForeignKey('tbc_rols.id_rol'), nullable=False)
    estatus_user = Column(Boolean, default=True, nullable=False)
    fecha_registro = Column(DateTime, nullable=False)
    fecha_modificacion = Column(DateTime, nullable=True)
    fecha_nacimiento = Column(Date, nullable=True)

    rol = relationship("Rols")

    def __repr__(self):
        return f"<User(id_user={self.id_user}, nombre_user='{self.nombre_user}', apellido_user='{self.apellido_user}', email_user='{self.email_user}', rol_id={self.rol_id}, estatus_user={self.estatus_user}, fecha_registro={self.fecha_registro}, fecha_modificacion={self.fecha_modificacion}, fecha_nacimiento={self.fecha_nacimiento})>"

    def to_dict(self):
        return {
            "id_user": self.id_user,
            "nombre_user": self.nombre_user,
            "apellido_user": self.apellido_user,
            "telefono_user": self.telefono_user,
            "email_user": self.email_user,
            "rol_id": self.rol_id,
            "estatus_user": self.estatus_user,
            "fecha_registro": self.fecha_registro,
            "fecha_modificacion": self.fecha_modificacion,
            "fecha_nacimiento": self.fecha_nacimiento
        }

    def from_dict(self, data):
        for field in ['nombre_user', 'apellido_user', 'telefono_user', 'email_user', 'password_user', 'rol_id', 'estatus_user', 'fecha_registro', 'fecha_modificacion', 'fecha_nacimiento']:
            if field in data:
                setattr(self, field, data[field])

    def __init__(self, nombre_user: str, apellido_user: str, telefono_user: str, email_user: str, password_user: str, rol_id: int, fecha_registro: DateTime, fecha_modificacion: DateTime = None, fecha_nacimiento: Date = None, estatus_user: bool = True):
        self.nombre_user = nombre_user
        self.apellido_user = apellido_user
        self.telefono_user = telefono_user
        self.email_user = email_user
        self.password_user = password_user
        self.rol_id = rol_id
        self.estatus_user = estatus_user
        self.fecha_registro = fecha_registro
        self.fecha_modificacion = fecha_modificacion
        self.fecha_nacimiento = fecha_nacimiento
    pass
# Fin del archivo models/modelUser.py
