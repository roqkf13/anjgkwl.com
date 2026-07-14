"""create player table

Revision ID: 0003_create_player_table
Revises: 0002_create_team_table
Create Date: 2026-07-13

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0003_create_player_table"
down_revision: Union[str, Sequence[str], None] = "0002_create_team_table"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "player",
        sa.Column("player_id", sa.String(10), primary_key=True),
        sa.Column("player_name", sa.String(20), nullable=True),
        sa.Column("e_player_name", sa.String(40), nullable=True),
        sa.Column("nickname", sa.String(30), nullable=True),
        sa.Column("join_yyyy", sa.String(10), nullable=True),
        sa.Column("position", sa.String(10), nullable=True),
        sa.Column("back_no", sa.Integer(), nullable=True),
        sa.Column("nation", sa.String(20), nullable=True),
        sa.Column("birth_date", sa.Date(), nullable=True),
        sa.Column("solar", sa.String(10), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("weight", sa.Integer(), nullable=True),
        sa.Column(
            "team_id",
            sa.String(10),
            sa.ForeignKey("team.team_id", ondelete="SET NULL", onupdate="CASCADE"),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_table("player")
