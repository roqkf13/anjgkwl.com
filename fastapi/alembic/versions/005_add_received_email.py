"""add sherlock_received_email table

Revision ID: 005_received_email
Revises: 004_unique_email
Create Date: 2026-07-01
"""
from alembic import op
import sqlalchemy as sa

revision = "005_received_email"
down_revision = "004_unique_email"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "sherlock_received_email",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("gmail_id", sa.String(), nullable=False, unique=True),
        sa.Column("thread_id", sa.String(), nullable=True),
        sa.Column("from_address", sa.String(), nullable=True),
        sa.Column("to", sa.String(), nullable=True),
        sa.Column("subject", sa.String(), nullable=True),
        sa.Column("snippet", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("sherlock_received_email")
