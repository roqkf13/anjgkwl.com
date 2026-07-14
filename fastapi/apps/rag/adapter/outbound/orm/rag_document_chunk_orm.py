from __future__ import annotations

from pgvector.sqlalchemy import Vector
from sqlalchemy import BigInteger, Integer, String, Text, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column

from core.matrix.gird_neo_theone_base import Base


class RagDocumentChunkOrm(Base):
    __tablename__ = "rag_document_chunks"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    document_name: Mapped[str] = mapped_column(String, nullable=False)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float]] = mapped_column(Vector(768), nullable=False)
    created_at: Mapped[object] = mapped_column(
        TIMESTAMP, nullable=False, server_default=func.now()
    )
