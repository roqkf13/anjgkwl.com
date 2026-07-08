from __future__ import annotations

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from core.matrix.gird_neo_theone_base import Base


class ScoutGenreTraitOrm(Base):
    __tablename__ = "scout_genre_traits"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    genre_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("scout_genres.id"), nullable=False
    )
    trait: Mapped[str] = mapped_column(String, nullable=False)
