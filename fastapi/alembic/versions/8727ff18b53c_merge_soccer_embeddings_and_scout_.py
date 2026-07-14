"""merge soccer embeddings and scout search heads

Revision ID: 8727ff18b53c
Revises: 0005_add_soccer_embeddings, 007_scout_search_entries
Create Date: 2026-07-14 03:02:12.791010

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8727ff18b53c'
down_revision: Union[str, Sequence[str], None] = ('0005_add_soccer_embeddings', '007_scout_search_entries')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
