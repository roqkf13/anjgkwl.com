"""create titanic_person and titanic_booking

Revision ID: 001_person_booking
Revises:
Create Date: 2026-06-04

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "001_person_booking"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "titanic_person",
        sa.Column("passenger_id", sa.String(length=32), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False, server_default=""),
        sa.Column("gender", sa.String(length=16), nullable=False, server_default=""),
        sa.Column("age", sa.String(length=16), nullable=False, server_default=""),
        sa.Column("sib_sp", sa.String(length=8), nullable=False, server_default=""),
        sa.Column("parch", sa.String(length=8), nullable=False, server_default=""),
        sa.Column("survived", sa.String(length=8), nullable=False, server_default=""),
        sa.PrimaryKeyConstraint("passenger_id"),
    )
    op.create_table(
        "titanic_booking",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("passenger_id", sa.String(length=32), nullable=False),
        sa.Column("pclass", sa.String(length=8), nullable=False, server_default=""),
        sa.Column("ticket", sa.String(length=64), nullable=False, server_default=""),
        sa.Column("fare", sa.String(length=32), nullable=False, server_default=""),
        sa.Column("cabin", sa.String(length=64), nullable=False, server_default=""),
        sa.Column("embarked", sa.String(length=8), nullable=False, server_default=""),
        sa.ForeignKeyConstraint(
            ["passenger_id"],
            ["titanic_person.passenger_id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_titanic_booking_passenger_id"),
        "titanic_booking",
        ["passenger_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_titanic_booking_passenger_id"), table_name="titanic_booking")
    op.drop_table("titanic_booking")
    op.drop_table("titanic_person")
