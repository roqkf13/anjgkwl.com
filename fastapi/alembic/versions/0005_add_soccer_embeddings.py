"""add embedding column to soccer tables

Revision ID: 0005_add_soccer_embeddings
Revises: 0004_create_schedule_table
Create Date: 2026-07-14

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

revision: str = "0005_add_soccer_embeddings"
down_revision: Union[str, Sequence[str], None] = "0004_create_schedule_table"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    for table in ("stadium", "team", "player", "schedule"):
        op.add_column(table, sa.Column("embedding", Vector(1536), nullable=True))


def downgrade() -> None:
    for table in ("stadium", "team", "player", "schedule"):
        op.drop_column(table, "embedding")
