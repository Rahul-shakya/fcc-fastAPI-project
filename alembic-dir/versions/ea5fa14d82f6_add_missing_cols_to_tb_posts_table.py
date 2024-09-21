"""Add missing cols to tb_posts table

Revision ID: ea5fa14d82f6
Revises: c6fd4a6eb24f
Create Date: 2024-09-21 17:14:55.787317

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ea5fa14d82f6'
down_revision: Union[str, None] = 'c6fd4a6eb24f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('tb_posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('tb_posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')))
    pass


def downgrade():
    op.drop_column('tb_posts', 'published')
    op.drop_column('tb_posts', 'created_at')
    pass