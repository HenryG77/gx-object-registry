"""Create object_types and genexus_objects tables

Revision ID: 001
Revises:
Create Date: 2026-07-29 15:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Crear tabla object_types
    op.create_table(
        'object_types',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, comment='Identificador único del tipo de objeto'),
        sa.Column('name', sa.String(length=100), nullable=False, comment='Nombre del tipo de objeto (ej: PROCEDURE, TRANSACTION)'),
        sa.Column('created_at', sa.DateTime(timezone=False), server_default=sa.text('now()'), nullable=False, comment='Fecha de creación'),
        sa.Column('updated_at', sa.DateTime(timezone=False), server_default=sa.text('now()'), nullable=False, comment='Fecha de última actualización'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name'),
        comment='Tipos de objetos de GeneXus'
    )

    # Crear índice case-insensitive para name
    op.create_index(
        'idx_object_types_name_lower',
        'object_types',
        [sa.text('lower(name)')],
        unique=True
    )

    # Crear tabla genexus_objects
    op.create_table(
        'genexus_objects',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, comment='Identificador único del objeto'),
        sa.Column('name', sa.String(length=128), nullable=False, comment='Nombre técnico del objeto GeneXus (ej: AhrPr001)'),
        sa.Column('description', sa.Text(), nullable=True, comment='Descripción funcional del objeto'),
        sa.Column('object_type_id', postgresql.UUID(as_uuid=True), nullable=False, comment='ID del tipo de objeto (FK a object_types)'),
        sa.Column('source_type', sa.Enum('MANUAL', 'CSV', name='source_type_enum', create_type=True), nullable=False, comment='Origen del registro (MANUAL o CSV)'),
        sa.Column('created_at', sa.DateTime(timezone=False), server_default=sa.text('now()'), nullable=False, comment='Fecha de creación'),
        sa.Column('updated_at', sa.DateTime(timezone=False), server_default=sa.text('now()'), nullable=False, comment='Fecha de última actualización'),
        sa.ForeignKeyConstraint(['object_type_id'], ['object_types.id'], ondelete='RESTRICT'),
        sa.PrimaryKeyConstraint('id'),
        comment='Objetos de GeneXus'
    )

    # Crear índices y restricciones para genexus_objects
    # Restricción de unicidad: (name, object_type_id)
    op.create_index(
        'uq_genexus_objects_name_type',
        'genexus_objects',
        ['name', 'object_type_id'],
        unique=True
    )

    # Índice para búsquedas por tipo
    op.create_index(
        'idx_genexus_objects_object_type_id',
        'genexus_objects',
        ['object_type_id']
    )

    # Índice para búsquedas por origen
    op.create_index(
        'idx_genexus_objects_source_type',
        'genexus_objects',
        ['source_type']
    )

    # Índice para ordenar por nombre
    op.create_index(
        'idx_genexus_objects_name',
        'genexus_objects',
        ['name']
    )

    # Índice para ordenar por fecha de creación (descendente)
    op.create_index(
        'idx_genexus_objects_created_at',
        'genexus_objects',
        [sa.text('created_at DESC')]
    )


def downgrade() -> None:
    # Eliminar índices de genexus_objects
    op.drop_index('idx_genexus_objects_created_at', table_name='genexus_objects')
    op.drop_index('idx_genexus_objects_name', table_name='genexus_objects')
    op.drop_index('idx_genexus_objects_source_type', table_name='genexus_objects')
    op.drop_index('idx_genexus_objects_object_type_id', table_name='genexus_objects')
    op.drop_index('uq_genexus_objects_name_type', table_name='genexus_objects')

    # Eliminar tabla genexus_objects
    op.drop_table('genexus_objects')

    # Eliminar tipo ENUM
    sa.Enum('MANUAL', 'CSV', name='source_type_enum').drop(op.get_bind())

    # Eliminar índice de object_types
    op.drop_index('idx_object_types_name_lower', table_name='object_types')

    # Eliminar tabla object_types
    op.drop_table('object_types')
