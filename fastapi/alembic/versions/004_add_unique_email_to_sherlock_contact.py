"""add unique constraint on e_mail_1_value in sherlock_contact

Revision ID: 004_add_unique_email_to_sherlock_contact
Revises: 003_create_sherlock_contact
Create Date: 2026-06-30

"""
from typing import Sequence, Union

from alembic import op

revision: str = "004_unique_email"
down_revision: Union[str, Sequence[str], None] = "003_create_sherlock_contact"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(
        "uq_sherlock_contact_email1",
        "sherlock_contact",
        ["e_mail_1_value"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_sherlock_contact_email1",
        "sherlock_contact",
        type_="unique",
    )
