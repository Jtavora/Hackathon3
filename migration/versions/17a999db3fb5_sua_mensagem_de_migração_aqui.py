"""Sua mensagem de migração aqui

Revision ID: 17a999db3fb5
Revises: ed741858b13d
Create Date: 2024-05-25 05:04:08.354198

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '17a999db3fb5'
down_revision: Union[str, None] = 'ed741858b13d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
