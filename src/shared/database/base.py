"""
Clase base para todos los modelos de SQLAlchemy.
"""
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Clase base para todos los modelos de la base de datos.

    Todos los modelos (ObjectTypeModel, GeneXusObjectModel, etc.)
    heredarán de esta clase.
    """
    pass
