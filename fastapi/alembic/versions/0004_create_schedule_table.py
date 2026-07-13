"""create schedule table

Revision ID: 0004_create_schedule_table
Revises: 0003_create_player_table
Create Date: 2026-07-13

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0004_create_schedule_table"
down_revision: Union[str, Sequence[str], None] = "0003_create_player_table"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "schedule",
        sa.Column("sche_date", sa.String(10), primary_key=True),
        sa.Column(
            "stadium_id",
            sa.String(10),
            sa.ForeignKey(
                "stadium.stadium_id", ondelete="RESTRICT", onupdate="CASCADE"
            ),
            primary_key=True,
        ),
        sa.Column("gubun", sa.String(10), nullable=True),
        sa.Column("hometeam_id", sa.String(10), nullable=True),
        sa.Column("awayteam_id", sa.String(10), nullable=True),
        sa.Column("home_score", sa.Integer(), nullable=True),
        sa.Column("away_score", sa.Integer(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("schedule")
