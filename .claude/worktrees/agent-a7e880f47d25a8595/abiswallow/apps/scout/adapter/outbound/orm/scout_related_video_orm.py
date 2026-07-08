from __future__ import annotations

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from core.matrix.gird_neo_theone_base import Base


class ScoutRelatedVideoOrm(Base):
    __tablename__ = "scout_related_videos"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    game_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("scout_games.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    channel: Mapped[str] = mapped_column(String, nullable=False)
    published_at: Mapped[str | None] = mapped_column(String, nullable=True)
    watch_url: Mapped[str] = mapped_column(String, nullable=False)
