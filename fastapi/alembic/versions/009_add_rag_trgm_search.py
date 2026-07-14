"""add pg_trgm extension and trigram index for rag hybrid search

Revision ID: 009_rag_trgm_search
Revises: 008_rag_document_chunks
Create Date: 2026-07-14
"""
from alembic import op

revision = "009_rag_trgm_search"
down_revision = "008_rag_document_chunks"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    op.execute(
        "CREATE INDEX ix_rag_document_chunks_content_trgm "
        "ON rag_document_chunks USING gin (content gin_trgm_ops)"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_rag_document_chunks_content_trgm")
