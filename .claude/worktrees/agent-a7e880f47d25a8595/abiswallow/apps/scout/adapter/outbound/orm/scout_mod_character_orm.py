from __future__ import annotations

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column
from core.matrix.gird_neo_theone_base import Base


class ScoutModCharacterOrm(Base):
    __tablename__ = "scout_mod_characters"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    mod_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("scout_mods.id"), nullable=False
    )
    character_slug: Mapped[str] = mapped_column(String, nullable=False)
