from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from rag.adapter.outbound.orm.rag_document_chunk_orm import RagDocumentChunkOrm
from rag.app.ports.output.rag_document_port import RagDocumentPort
from rag.domain.entities.rag_document_chunk_entity import RagDocumentChunkEntity


class RagDocumentRepository(RagDocumentPort):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save_chunks(self, chunks: list[RagDocumentChunkEntity]) -> None:
        self._session.add_all(
            RagDocumentChunkOrm(
                document_name=chunk.document_name,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                embedding=chunk.embedding,
            )
            for chunk in chunks
        )
        await self._session.commit()

    async def search_similar(
        self, embedding: list[float], limit: int = 4
    ) -> list[RagDocumentChunkEntity]:
        stmt = (
            select(RagDocumentChunkOrm)
            .order_by(RagDocumentChunkOrm.embedding.cosine_distance(embedding))
            .limit(limit)
        )
        result = await self._session.execute(stmt)
        return [
            RagDocumentChunkEntity(
                id=row.id,
                document_name=row.document_name,
                chunk_index=row.chunk_index,
                content=row.content,
                embedding=list(row.embedding),
            )
            for row in result.scalars().all()
        ]
