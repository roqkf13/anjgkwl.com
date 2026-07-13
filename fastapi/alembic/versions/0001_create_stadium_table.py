"""create stadium table

Revision ID: 0001_create_stadium_table
Revises: 006_received_email_embedding
Create Date: 2026-07-13

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0001_create_stadium_table"
down_revision: Union[str, Sequence[str], None] = "006_received_email_embedding"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "stadium",
        sa.Column("stadium_id", sa.String(10), primary_key=True),
        sa.Column("statdium_name", sa.String(40), nullable=True),
        sa.Column("hometeam_id", sa.String(10), nullable=True),
        sa.Column("seat_count", sa.Integer(), nullable=True),
        sa.Column("address", sa.String(60), nullable=True),
        sa.Column("ddd", sa.String(10), nullable=True),
        sa.Column("tel", sa.String(10), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("stadium")
