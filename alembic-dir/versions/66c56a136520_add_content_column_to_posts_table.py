"""Add content column to posts table

Revision ID: 66c56a136520
Revises: 2053a3133596
Create Date: 2024-09-21 15:11:20.542411

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '66c56a136520'
down_revision: Union[str, None] = '2053a3133596'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('tb_posts', sa.Column('content', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    op.drop_column('tb_posts', 'content')
    pass
