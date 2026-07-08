"""create sherlock_contact table

Revision ID: 003_create_sherlock_contact
Revises: d996c60cb717
Create Date: 2026-06-30

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "003_create_sherlock_contact"
down_revision: Union[str, Sequence[str], None] = "d996c60cb717"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "sherlock_contact",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("first_name", sa.String(), nullable=True),
        sa.Column("middle_name", sa.String(), nullable=True),
        sa.Column("last_name", sa.String(), nullable=True),
        sa.Column("phonetic_first_name", sa.String(), nullable=True),
        sa.Column("phonetic_middle_name", sa.String(), nullable=True),
        sa.Column("phonetic_last_name", sa.String(), nullable=True),
        sa.Column("name_prefix", sa.String(), nullable=True),
        sa.Column("name_suffix", sa.String(), nullable=True),
        sa.Column("nickname", sa.String(), nullable=True),
        sa.Column("file_as", sa.String(), nullable=True),
        sa.Column("organization_name", sa.String(), nullable=True),
        sa.Column("organization_title", sa.String(), nullable=True),
        sa.Column("organization_department", sa.String(), nullable=True),
        sa.Column("birthday", sa.String(), nullable=True),
        sa.Column("notes", sa.String(), nullable=True),
        sa.Column("photo", sa.String(), nullable=True),
        sa.Column("labels", sa.String(), nullable=True),
        sa.Column("e_mail_1_label", sa.String(), nullable=True),
        sa.Column("e_mail_1_value", sa.String(), nullable=True),
        sa.Column("e_mail_2_label", sa.String(), nullable=True),
        sa.Column("e_mail_2_value", sa.String(), nullable=True),
        sa.Column("phone_1_label", sa.String(), nullable=True),
        sa.Column("phone_1_value", sa.String(), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("sherlock_contact")
