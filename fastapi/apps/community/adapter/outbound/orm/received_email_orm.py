from __future__ import annotations

import uuid

from pgvector.sqlalchemy import Vector
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from core.matrix.gird_neo_theone_base import Base


class ReceivedEmailOrm(Base):
    __tablename__ = "sherlock_received_email"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    gmail_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    thread_id: Mapped[str | None] = mapped_column(String, nullable=True)
    from_: Mapped[str | None] = mapped_column("from_address", String, nullable=True)
    to: Mapped[str | None] = mapped_column(String, nullable=True)
    subject: Mapped[str | None] = mapped_column(String, nullable=True)
    snippet: Mapped[str | None] = mapped_column(Text, nullable=True)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(768), nullable=True)
