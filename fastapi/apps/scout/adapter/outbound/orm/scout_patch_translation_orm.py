from __future__ import annotations

from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from core.matrix.gird_neo_theone_base import Base


class ScoutPatchTranslationOrm(Base):
    __tablename__ = "scout_patch_translations"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    patch_note_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("scout_patch_notes.id"), nullable=False
    )
    locale: Mapped[str] = mapped_column(String, nullable=False)
    translated_title: Mapped[str | None] = mapped_column(String, nullable=True)
    translated_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    translated_body: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_urls: Mapped[list | None] = mapped_column(JSON, nullable=True)
    translated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
