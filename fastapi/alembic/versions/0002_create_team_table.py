"""create team table

Revision ID: 0002_create_team_table
Revises: 0001_create_stadium_table
Create Date: 2026-07-13

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002_create_team_table"
down_revision: Union[str, Sequence[str], None] = "0001_create_stadium_table"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "team",
        sa.Column("team_id", sa.String(10), primary_key=True),
        sa.Column("region_name", sa.String(10), nullable=True),
        sa.Column("team_name", sa.String(40), nullable=True),
        sa.Column("e_team_name", sa.String(50), nullable=True),
        sa.Column("orig_yyyy", sa.String(10), nullable=True),
        sa.Column("zip_code1", sa.String(10), nullable=True),
        sa.Column("zip_code2", sa.String(10), nullable=True),
        sa.Column("address", sa.String(80), nullable=True),
        sa.Column("ddd", sa.String(10), nullable=True),
        sa.Column("tel", sa.String(10), nullable=True),
        sa.Column("fax", sa.String(10), nullable=True),
        sa.Column("homepage", sa.String(50), nullable=True),
        sa.Column("owner", sa.String(10), nullable=True),
        sa.Column(
            "stadium_id",
            sa.String(10),
            sa.ForeignKey(
                "stadium.stadium_id", ondelete="SET NULL", onupdate="CASCADE"
            ),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_table("team")
