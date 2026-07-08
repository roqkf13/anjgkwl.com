from __future__ import annotations

from sqlalchemy import BigInteger, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from core.matrix.gird_neo_theone_base import Base


class ScoutPatchNoteOrm(Base):
    __tablename__ = "scout_patch_notes"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    game_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("scout_games.id"), nullable=False
    )
    external_note_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    source_title: Mapped[str] = mapped_column(String, nullable=False)
    source_summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    source_body: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_urls: Mapped[list | None] = mapped_column(JSON, nullable=True)
    published_at: Mapped[str | None] = mapped_column(String, nullable=True)
    source_url: Mapped[str | None] = mapped_column(String, nullable=True)
