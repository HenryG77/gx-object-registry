"""
Modelos SQLAlchemy para object_types.
"""
from sqlalchemy import Column, String, DateTime, Index, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from src.shared.database.base import Base


class ObjectTypeModel(Base):
    """
    Modelo SQLAlchemy para la tabla object_types.

    Mapea la entidad de dominio ObjectType a la base de datos PostgreSQL.
    """

    __tablename__ = "object_types"

    # Columnas
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Identificador único del tipo de objeto",
    )

    name = Column(
        String(100),
        nullable=False,
        unique=True,
        comment="Nombre del tipo de objeto (ej: PROCEDURE, TRANSACTION)",
    )

    created_at = Column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now(),
        comment="Fecha de creación",
    )

    updated_at = Column(
        DateTime(timezone=False),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
        comment="Fecha de última actualización",
    )

    # Relaciones (se configurarán cuando creemos genexus_objects)
    # genexus_objects = relationship("GeneXusObjectModel", back_populates="object_type")

    # Índices
    __table_args__ = (
        # Índice para búsquedas case-insensitive
        Index("idx_object_types_name_lower", func.lower(name), unique=True),
        # Constraint para validar que name no esté vacío
        {"comment": "Catálogo de tipos de objetos GeneXus"},
    )

    def __repr__(self) -> str:
        return f"<ObjectTypeModel(id={self.id}, name={self.name})>"
