"""Add last_login to users

Revision ID: a1b2c3d4e5f6
Revises: 55adc69b9133
Create Date: 2026-08-01 11:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '55adc69b9133'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Agregar campo last_login a la tabla users
    op.add_column('users', sa.Column('last_login', sa.DateTime(), nullable=True, comment='Fecha y hora del último login'))


def downgrade() -> None:
    # Eliminar campo last_login de la tabla users
    op.drop_column('users', 'last_login')
