"""Add must_change_password to users

Revision ID: b2c3d4e5f6g7
Revises: a1b2c3d4e5f6
Create Date: 2026-08-01 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'b2c3d4e5f6g7'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Agregar campo must_change_password a la tabla users
    op.add_column('users', sa.Column(
        'must_change_password',
        sa.Boolean(),
        nullable=False,
        server_default='false',
        comment='Indica si el usuario debe cambiar su contraseña en el próximo login'
    ))


def downgrade() -> None:
    # Eliminar campo must_change_password de la tabla users
    op.drop_column('users', 'must_change_password')
