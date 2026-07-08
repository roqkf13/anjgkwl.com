from __future__ import annotations

from sqlalchemy import BigInteger, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from core.matrix.gird_neo_theone_base import Base


class ScoutGameOrm(Base):
    __tablename__ = "scout_games"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    genre_id: Mapped[int | None] = mapped_column(
        BigInteger, ForeignKey("scout_genres.id"), nullable=True
    )
    steam_app_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    official_site_url: Mapped[str | None] = mapped_column(String, nullable=True)
