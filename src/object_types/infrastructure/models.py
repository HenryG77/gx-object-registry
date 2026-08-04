"""
Modelos SQLAlchemy para object_types.
"""
from sqlalchemy import Column, String, DateTime, Index, Integer, ForeignKey, func
from sqlalchemy.orm import relationship

from src.shared.database.base import Base


class ObjectTypeModel(Base):
    """
    Modelo SQLAlchemy para la tabla object_types.

    Mapea la entidad de dominio ObjectType a la base de datos PostgreSQL.
    """

    __tablename__ = "object_types"

    # Columnas
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=False,  # Permite IDs manuales y automáticos
        comment="Identificador único del tipo de objeto (puede ser manual o autoincremental)",
    )

    name = Column(
        String(100),
        nullable=False,
        unique=True,
        comment="Nombre del tipo de objeto (ej: PROCEDURE, TRANSACTION)",
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        comment="Usuario que creó el registro",
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

    # Relaciones
    creator = relationship(
        "UserModel",
        foreign_keys=[created_by],
        lazy="select",
    )

    # Índices
    __table_args__ = (
        # Índice para búsquedas case-insensitive
        Index("idx_object_types_name_lower", func.lower(name), unique=True),
        # Constraint para validar que name no esté vacío
        {"comment": "Catálogo de tipos de objetos GeneXus"},
    )

    def __repr__(self) -> str:
        return f"<ObjectTypeModel(id={self.id}, name={self.name})>"
