from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from rag.adapter.outbound.orm.rag_document_chunk_orm import RagDocumentChunkOrm
from rag.app.ports.output.rag_document_port import RagDocumentPort
from rag.domain.entities.rag_document_chunk_entity import RagDocumentChunkEntity
from rag.domain.rag_keyword_matching import extract_keyword_candidates


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
        """벡터 유사도 검색과 키워드 부분일치 검색을 합친다.

        고유명사·별명처럼 의미보다 문자열 자체가 중요한 질문은 임베딩 코사인
        유사도만으로는 순위가 크게 밀려 top_k 밖으로 빠지는 경우가 많다.
        문장 전체를 trigram으로 비교하면 질문이 길수록 짧은 일치가 희석돼
        점수가 낮아지므로, 질문에서 뽑은 부분 문자열 키워드로 직접
        ILIKE 매칭해 보완한다 (긴 키워드=더 구체적인 일치부터 시도).
        """
        vector_stmt = (
            select(RagDocumentChunkOrm)
            .order_by(RagDocumentChunkOrm.embedding.cosine_distance(embedding))
            .limit(limit)
        )
        vector_rows = list((await self._session.execute(vector_stmt)).scalars().all())

        # 후보를 전부 조회한 뒤, 각 청크가 매칭된 키워드 중 가장 긴(=가장 구체적인)
        # 길이로 순위를 매긴다. 도중에 멈추면 후보 순서(파이썬 set 반복은
        # 프로세스마다 순서가 달라짐)에 따라 결과가 들쭉날쭉해지므로 전부 모아서 정렬한다.
        seen_ids = {row.id for row in vector_rows}
        best_match_len: dict[int, int] = {}
        matched_rows: dict[int, RagDocumentChunkOrm] = {}
        for keyword in extract_keyword_candidates(query_text):
            keyword_stmt = select(RagDocumentChunkOrm).where(
                RagDocumentChunkOrm.content.ilike(f"%{keyword}%")
            )
            for row in (await self._session.execute(keyword_stmt)).scalars().all():
                if row.id in seen_ids:
                    continue
                if len(keyword) > best_match_len.get(row.id, 0):
                    best_match_len[row.id] = len(keyword)
                    matched_rows[row.id] = row

        keyword_rows = sorted(
            matched_rows.values(), key=lambda row: best_match_len[row.id], reverse=True
        )[:limit]

        return [
            RagDocumentChunkEntity(
                id=row.id,
                document_name=row.document_name,
                chunk_index=row.chunk_index,
                content=row.content,
                embedding=list(row.embedding),
            )
            for row in [*vector_rows, *keyword_rows]
        ]
