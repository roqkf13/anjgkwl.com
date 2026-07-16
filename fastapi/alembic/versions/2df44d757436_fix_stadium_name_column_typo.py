"""fix stadium_name column typo

Revision ID: 2df44d757436
Revises: 009_rag_trgm_search
Create Date: 2026-07-15 07:50:05.952527

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2df44d757436'
down_revision: Union[str, Sequence[str], None] = '009_rag_trgm_search'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.alter_column('stadium', 'statdium_name', new_column_name='stadium_name')

def downgrade():
    op.alter_column('stadium', 'stadium_name', new_column_name='statdium_name')