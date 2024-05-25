"""Login

Revision ID: 64fc794ee92b
Revises: f7abfc0a9129
Create Date: 2024-05-25 12:53:57.216181

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '64fc794ee92b'
down_revision: Union[str, None] = 'f7abfc0a9129'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('respostas_aluno', 'status',
               existing_type=postgresql.ENUM('PENDENTE', 'CORRETA', 'INCORRETA', name='statusresposta'),
               type_=sa.String(length=300),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('respostas_aluno', 'status',
               existing_type=sa.String(length=300),
               type_=postgresql.ENUM('PENDENTE', 'CORRETA', 'INCORRETA', name='statusresposta'),
               nullable=True)
    # ### end Alembic commands ###