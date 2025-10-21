from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .database import Base
from .database import engine
import datetime


# --- Modelos SQLAlchemy (Representación de las tablas) ---

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    nombre = Column(String)
    hashed_password = Column(String, nullable=False)

    # Relaciones
    transacciones = relationship("Transaccion", back_populates="propietario")
    categorias = relationship("Categoria", back_populates="propietario")

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, index=True, nullable=False)
    tipo = Column(String, nullable=False) # "ingreso" o "gasto"
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    # Relaciones
    propietario = relationship("Usuario", back_populates="categorias")

class Transaccion(Base):
    __tablename__ = "transacciones"

    id = Column(Integer, primary_key=True, index=True)
    monto = Column(Float, nullable=False)
    fecha = Column(DateTime, default=datetime.datetime.utcnow)
    descripcion = Column(String, index=True)
    tipo = Column(String, nullable=False) # "ingreso" o "gasto"
    
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

    # Relaciones
    propietario = relationship("Usuario", back_populates="transacciones")

# --- Función para crear la base de datos y las tablas ---
def crear_db():
    Base.metadata.create_all(bind=engine)