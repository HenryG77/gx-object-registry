"""Create ID sequences for object_types and genexus_objects

Revision ID: 20260806_1700
Revises: 20260801_1200_add_must_change_password
Create Date: 2026-08-06 17:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20260806_1700'
down_revision: Union[str, None] = 'b2c3d4e5f6g7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Crear secuencia para object_types
    op.execute("""
        CREATE SEQUENCE IF NOT EXISTS object_types_id_seq
        START WITH 0
        INCREMENT BY 1
        MINVALUE 0
        NO MAXVALUE
        CACHE 1;
    """)

    # Asociar secuencia con la columna id de object_types
    op.execute("""
        ALTER TABLE object_types
        ALTER COLUMN id SET DEFAULT nextval('object_types_id_seq');
    """)

    # Hacer que la secuencia sea propiedad de la columna
    op.execute("""
        ALTER SEQUENCE object_types_id_seq OWNED BY object_types.id;
    """)

    # Crear secuencia para genexus_objects
    op.execute("""
        CREATE SEQUENCE IF NOT EXISTS genexus_objects_id_seq
        START WITH 1
        INCREMENT BY 1
        MINVALUE 1
        NO MAXVALUE
        CACHE 1;
    """)

    # Asociar secuencia con la columna id de genexus_objects
    op.execute("""
        ALTER TABLE genexus_objects
        ALTER COLUMN id SET DEFAULT nextval('genexus_objects_id_seq');
    """)

    # Hacer que la secuencia sea propiedad de la columna
    op.execute("""
        ALTER SEQUENCE genexus_objects_id_seq OWNED BY genexus_objects.id;
    """)


def downgrade() -> None:
    # Eliminar default de genexus_objects
    op.execute("""
        ALTER TABLE genexus_objects
        ALTER COLUMN id DROP DEFAULT;
    """)

    # Eliminar secuencia de genexus_objects
    op.execute("DROP SEQUENCE IF EXISTS genexus_objects_id_seq;")

    # Eliminar default de object_types
    op.execute("""
        ALTER TABLE object_types
        ALTER COLUMN id DROP DEFAULT;
    """)

    # Eliminar secuencia de object_types
    op.execute("DROP SEQUENCE IF EXISTS object_types_id_seq;")
