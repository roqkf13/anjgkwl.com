from __future__ import annotations

from abc import ABC, abstractmethod

from rag.adapter.inbound.api.schemas.rag_chat_schema import RagChatResponseSchema, RagChatSchema
from rag.adapter.inbound.api.schemas.rag_document_schema import RagUploadResponseSchema


class RagDocumentUseCase(ABC):

    @abstractmethod
    async def upload_document(
        self, filename: str, content_type: str, text: str
    ) -> RagUploadResponseSchema:
        """문서를 청크로 분할하고 임베딩을 생성해 저장한다."""

    @abstractmethod
    async def ask(self, schema: RagChatSchema) -> RagChatResponseSchema:
        """질문과 관련된 문서 청크를 검색해 답변을 생성한다."""
