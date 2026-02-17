'''
Docstring for config.db
Este archivo configura la conexión a la base de datos utilizando SQLAlchemy. Define la URL de la base de datos, crea el motor de conexión, la sesión local y la base declarativa para los modelos.
'''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite://root:1234@localhost:3307/autolavado_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
