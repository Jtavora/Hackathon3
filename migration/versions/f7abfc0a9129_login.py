"""Login

Revision ID: f7abfc0a9129
Revises: 529ff2d5597a
Create Date: 2024-05-25 09:56:34.674952

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'f7abfc0a9129'
down_revision: Union[str, None] = '529ff2d5597a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('alunos', sa.Column('senha', sa.String(length=100), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('alunos', 'senha')
    # ### end Alembic commands ###
