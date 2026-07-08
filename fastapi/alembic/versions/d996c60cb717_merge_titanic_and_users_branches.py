"""merge_titanic_and_users_branches

Revision ID: d996c60cb717
Revises: 002_booking_passenger_unique, f0ccee9b49fe
Create Date: 2026-06-17 08:28:46.933374

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd996c60cb717'
down_revision: Union[str, Sequence[str], None] = ('002_booking_passenger_unique', 'f0ccee9b49fe')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
