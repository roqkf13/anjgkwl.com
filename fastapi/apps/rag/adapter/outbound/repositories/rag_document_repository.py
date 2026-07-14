from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from rag.adapter.outbound.orm.rag_document_chunk_orm import RagDocumentChunkOrm
from rag.app.ports.output.rag_document_port import RagDocumentPort
from rag.domain.entities.rag_document_chunk_entity import RagDocumentChunkEntity

_TRGM_SIMILARITY_MIN = 0.01


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
        self, embedding: list[float], limit: int = 4, query_text: str = ""
    ) -> list[RagDocumentChunkEntity]:
        """벡터 유사도 검색과 trigram 키워드 검색을 합친다.

        고유명사·별명처럼 의미보다 문자열 자체가 중요한 질문은 임베딩 코사인
        유사도만으로는 순위가 크게 밀려 top_k 밖으로 빠지는 경우가 많아,
        pg_trgm 기반 키워드 매칭 결과를 함께 합쳐 보완한다.
        """
        vector_stmt = (
            select(RagDocumentChunkOrm)
            .order_by(RagDocumentChunkOrm.embedding.cosine_distance(embedding))
            .limit(limit)
        )
        vector_rows = (await self._session.execute(vector_stmt)).scalars().all()

        trgm_rows: list[RagDocumentChunkOrm] = []
        if query_text.strip():
            trgm_stmt = (
                select(RagDocumentChunkOrm)
                .where(func.similarity(RagDocumentChunkOrm.content, query_text) > _TRGM_SIMILARITY_MIN)
                .order_by(func.similarity(RagDocumentChunkOrm.content, query_text).desc())
                .limit(limit)
            )
            trgm_rows = (await self._session.execute(trgm_stmt)).scalars().all()

        merged: dict[int, RagDocumentChunkOrm] = {}
        for row in [*vector_rows, *trgm_rows]:
            merged.setdefault(row.id, row)

        return [
            RagDocumentChunkEntity(
                id=row.id,
                document_name=row.document_name,
                chunk_index=row.chunk_index,
                content=row.content,
                embedding=list(row.embedding),
            )
            for row in merged.values()
        ]
