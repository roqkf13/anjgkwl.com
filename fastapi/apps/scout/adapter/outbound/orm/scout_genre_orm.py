from __future__ import annotations

from sqlalchemy import BigInteger, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from core.matrix.gird_neo_theone_base import Base


class ScoutGenreOrm(Base):
    __tablename__ = "scout_genres"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    label: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    representative_game_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("scout_games.id", use_alter=True, name="fk_genre_rep_game"),
        nullable=True,
    )
