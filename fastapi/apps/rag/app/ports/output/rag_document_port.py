from __future__ import annotations

from abc import ABC, abstractmethod

from rag.domain.entities.rag_document_chunk_entity import RagDocumentChunkEntity


class RagDocumentPort(ABC):

    @abstractmethod
    async def save_chunks(self, chunks: list[RagDocumentChunkEntity]) -> None:
        """청크 목록을 벡터 임베딩과 함께 저장한다."""

    @abstractmethod
    async def search_similar(
        self, embedding: list[float], limit: int = 4, query_text: str = ""
    ) -> list[RagDocumentChunkEntity]:
        """임베딩 유사도와 query_text의 trigram 키워드 매칭을 함께 고려해 청크를 검색한다."""
