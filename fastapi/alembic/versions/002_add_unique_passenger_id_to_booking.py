"""add unique constraint on titanic_booking.passenger_id

Revision ID: 002_booking_passenger_unique
Revises: 001_person_booking
Create Date: 2026-06-17

"""

from typing import Sequence, Union

from alembic import op

revision: str = "002_booking_passenger_unique"
down_revision: Union[str, Sequence[str], None] = "001_person_booking"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_titanic_booking_passenger_id")
    op.create_index(
        "ix_titanic_booking_passenger_id",
        "titanic_booking",
        ["passenger_id"],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("ix_titanic_booking_passenger_id", table_name="titanic_booking")
    op.create_index(
        "ix_titanic_booking_passenger_id",
        "titanic_booking",
        ["passenger_id"],
        unique=False,
    )
