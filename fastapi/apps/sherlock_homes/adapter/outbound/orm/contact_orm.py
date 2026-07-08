from __future__ import annotations

import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from core.matrix.gird_neo_theone_base import Base


class ContactOrm(Base):
    __tablename__ = "sherlock_contact"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    first_name: Mapped[str | None] = mapped_column(String, nullable=True)
    middle_name: Mapped[str | None] = mapped_column(String, nullable=True)
    last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    phonetic_first_name: Mapped[str | None] = mapped_column(String, nullable=True)
    phonetic_middle_name: Mapped[str | None] = mapped_column(String, nullable=True)
    phonetic_last_name: Mapped[str | None] = mapped_column(String, nullable=True)
    name_prefix: Mapped[str | None] = mapped_column(String, nullable=True)
    name_suffix: Mapped[str | None] = mapped_column(String, nullable=True)
    nickname: Mapped[str | None] = mapped_column(String, nullable=True)
    file_as: Mapped[str | None] = mapped_column(String, nullable=True)
    organization_name: Mapped[str | None] = mapped_column(String, nullable=True)
    organization_title: Mapped[str | None] = mapped_column(String, nullable=True)
    organization_department: Mapped[str | None] = mapped_column(String, nullable=True)
    birthday: Mapped[str | None] = mapped_column(String, nullable=True)
    notes: Mapped[str | None] = mapped_column(String, nullable=True)
    photo: Mapped[str | None] = mapped_column(String, nullable=True)
    labels: Mapped[str | None] = mapped_column(String, nullable=True)
    e_mail_1_label: Mapped[str | None] = mapped_column(String, nullable=True)
    e_mail_1_value: Mapped[str | None] = mapped_column(String, nullable=True)
    e_mail_2_label: Mapped[str | None] = mapped_column(String, nullable=True)
    e_mail_2_value: Mapped[str | None] = mapped_column(String, nullable=True)
    phone_1_label: Mapped[str | None] = mapped_column(String, nullable=True)
    phone_1_value: Mapped[str | None] = mapped_column(String, nullable=True)
