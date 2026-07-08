"""add users table with age column

Revision ID: f0ccee9b49fe
Revises:
Create Date: 2026-05-19 16:43:36.059248

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = 'f0ccee9b49fe'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('name', sa.String(length=120), nullable=False, server_default=''),
        sa.Column('email', sa.String(length=255), nullable=False, server_default=''),
        sa.Column('password_hash', sa.String(length=255), nullable=False, server_default=''),
        sa.Column('role', sa.String(length=20), nullable=False, server_default='user'),
        sa.Column('user_id', sa.String(length=255), nullable=False, server_default=''),
        sa.Column('age', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_user_id'), 'users', ['user_id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_users_user_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
