"""
Modelos SQLAlchemy para genexus_objects.
"""
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Index, Enum, Integer, func
from sqlalchemy.orm import relationship
import enum

from src.shared.database.base import Base


class SourceTypeEnum(str, enum.Enum):
    """Enumeración para el origen del registro."""
    MANUAL = "MANUAL"
    CSV = "CSV"


class GeneXusObjectModel(Base):
    """
    Modelo SQLAlchemy para la tabla genexus_objects.

    Mapea la entidad de dominio GeneXusObject a la base de datos PostgreSQL.
    """

    __tablename__ = "genexus_objects"

    # Columnas
    id = Column(
        Integer,
        primary_key=True,
        autoincrement=False,  # Permite IDs manuales y automáticos
        comment="Identificador único del objeto (puede ser manual o autoincremental)",
    )

    name = Column(
        String(128),
        nullable=False,
        comment="Nombre técnico del objeto GeneXus (ej: AhrPr001)",
    )

    description = Column(
        Text,
        nullable=True,
        comment="Descripción funcional del objeto",
    )

    object_type_id = Column(
        Integer,
        ForeignKey("object_types.id", ondelete="RESTRICT"),
        nullable=False,
        comment="ID del tipo de objeto (FK a object_types)",
    )

    source_type = Column(
        Enum(SourceTypeEnum, name="source_type_enum", create_type=True),
        nullable=False,
        comment="Origen del registro (MANUAL o CSV)",
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
    object_type = relationship(
        "ObjectTypeModel",
        backref="genexus_objects",
        lazy="joined",  # Carga eager por defecto
    )

    creator = relationship(
        "UserModel",
        foreign_keys=[created_by],
        lazy="select",
    )

    # Índices y restricciones
    __table_args__ = (
        # Restricción de unicidad: (name, object_type_id)
        Index(
            "uq_genexus_objects_name_type",
            name,
            object_type_id,
            unique=True,
        ),
        # Índice para búsquedas por tipo
        Index("idx_genexus_objects_object_type_id", object_type_id),
        # Índice para búsquedas por origen
        Index("idx_genexus_objects_source_type", source_type),
        # Índice para ordenar por nombre
        Index("idx_genexus_objects_name", name),
        # Índice para ordenar por fecha de creación
        Index("idx_genexus_objects_created_at", created_at.desc()),
        # Índices GIN para búsqueda full-text (requiere extensión pg_trgm)
        # Index("idx_genexus_objects_name_trgm", name, postgresql_using="gin", postgresql_ops={"name": "gin_trgm_ops"}),
        # Index("idx_genexus_objects_description_trgm", description, postgresql_using="gin", postgresql_ops={"description": "gin_trgm_ops"}),
        {"comment": "Objetos de GeneXus"},
    )

    def __repr__(self) -> str:
        return f"<GeneXusObjectModel(id={self.id}, name={self.name}, type={self.object_type_id})>"
