from __future__ import annotations

from sqlalchemy import BigInteger, String, Text, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from core.matrix.gird_neo_theone_base import Base


class ScoutSearchEntryOrm(Base):
    __tablename__ = "scout_search_entries"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    query_key: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    platform: Mapped[str | None] = mapped_column(String, nullable=True)
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    official_site_url: Mapped[str | None] = mapped_column(String, nullable=True)
    videos: Mapped[list] = mapped_column(JSONB, nullable=False, server_default="[]")
    created_at: Mapped[object] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now()
    )
    updated_at: Mapped[object] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now()
    )
