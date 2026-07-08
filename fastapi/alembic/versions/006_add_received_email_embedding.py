"""add embedding column to sherlock_received_email

Revision ID: 006_received_email_embedding
Revises: 005_received_email
Create Date: 2026-07-02
"""
from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

revision = "006_received_email_embedding"
down_revision = "005_received_email"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.add_column(
        "sherlock_received_email",
        sa.Column("embedding", Vector(768), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("sherlock_received_email", "embedding")
