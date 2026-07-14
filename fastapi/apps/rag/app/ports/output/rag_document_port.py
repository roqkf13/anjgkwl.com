from __future__ import annotations

from abc import ABC, abstractmethod

from rag.domain.entities.rag_document_chunk_entity import RagDocumentChunkEntity


class RagDocumentPort(ABC):

    @abstractmethod
    async def save_chunks(self, chunks: list[RagDocumentChunkEntity]) -> None:
        """청크 목록을 벡터 임베딩과 함께 저장한다."""

    @abstractmethod
    async def search_similar(
        self, embedding: list[float], limit: int = 4
    ) -> list[RagDocumentChunkEntity]:
        """임베딩과 가장 유사한 청크를 검색한다."""
