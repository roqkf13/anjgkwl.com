from __future__ import annotations

from sqlalchemy import BigInteger, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from core.matrix.gird_neo_theone_base import Base


class ScoutPatchContentBlockOrm(Base):
    __tablename__ = "scout_patch_content_blocks"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    translation_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("scout_patch_translations.id"), nullable=False
    )
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False)
    block_type: Mapped[str] = mapped_column(String, nullable=False)
    text: Mapped[str | None] = mapped_column(Text, nullable=True)
    url: Mapped[str | None] = mapped_column(String, nullable=True)
