"""create scout_search_entries table

Revision ID: 007_scout_search_entries
Revises: 006_received_email_embedding
Create Date: 2026-07-13
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

revision = "007_scout_search_entries"
down_revision = "006_received_email_embedding"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "scout_search_entries",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("query_key", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("platform", sa.String(), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("official_site_url", sa.String(), nullable=True),
        sa.Column("videos", JSONB(), nullable=False, server_default="[]"),
        sa.Column(
            "created_at", sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()
        ),
        sa.Column(
            "updated_at", sa.TIMESTAMP(), nullable=False, server_default=sa.func.now()
        ),
    )
    op.create_unique_constraint(
        "uq_scout_search_entries_query_key", "scout_search_entries", ["query_key"]
    )


def downgrade() -> None:
    op.drop_table("scout_search_entries")
