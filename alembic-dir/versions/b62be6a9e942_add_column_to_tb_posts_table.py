"""Add column to tb_posts table

Revision ID: b62be6a9e942
Revises: dfbc9d0efced
Create Date: 2024-09-21 16:38:53.095852

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b62be6a9e942'
down_revision: Union[str, None] = 'dfbc9d0efced'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('tb_posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('tb_posts', 'content')
    pass