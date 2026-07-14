from __future__ import annotations

import asyncio
import logging

from rag.adapter.inbound.api.schemas.rag_chat_schema import RagChatResponseSchema, RagChatSchema
from rag.adapter.inbound.api.schemas.rag_document_schema import RagUploadResponseSchema
from rag.app.ports.input.rag_document_use_case import RagDocumentUseCase
from rag.app.ports.output.rag_document_port import RagDocumentPort
from rag.domain.entities.rag_document_chunk_entity import RagDocumentChunkEntity
from rag.domain.rag_chunking import split_into_chunks, split_sql_into_chunks

logger = logging.getLogger(__name__)

_TOP_K = 4


class RagDocumentInteractor(RagDocumentUseCase):

    def __init__(self, repository: RagDocumentPort) -> None:
        self.repository = repository

    async def upload_document(
        self, filename: str, content_type: str, text: str
    ) -> RagUploadResponseSchema:
        from core.matrix.ollama_neo_local_model import generate_embedding_ollama

        size_bytes = len(text.encode("utf-8"))
        chunk_texts = (
            split_sql_into_chunks(text) if filename.lower().endswith(".sql") else split_into_chunks(text)
        )
        if not chunk_texts:
            return RagUploadResponseSchema(
                filename=filename,
                content_type=content_type,
                size_bytes=size_bytes,
                chunk_count=0,
                message="문서에서 추출된 텍스트가 없습니다.",
            )

        embeddings = await asyncio.gather(
            *(asyncio.to_thread(generate_embedding_ollama, text=chunk) for chunk in chunk_texts)
        )
        chunks = [
            RagDocumentChunkEntity(
                id=None,
                document_name=filename,
                chunk_index=idx,
                content=chunk_text,
                embedding=embedding,
            )
            for idx, (chunk_text, embedding) in enumerate(zip(chunk_texts, embeddings))
        ]
        await self.repository.save_chunks(chunks)

        return RagUploadResponseSchema(
            filename=filename,
            content_type=content_type,
            size_bytes=size_bytes,
            chunk_count=len(chunks),
            message=f"{len(chunks)}개 청크로 분할되어 저장되었습니다.",
        )

    async def ask(self, schema: RagChatSchema) -> RagChatResponseSchema:
        from core.matrix.ollama_neo_local_model import generate_embedding_ollama, generate_reply_ollama

        question = next(
            (m.text for m in reversed(schema.messages) if m.role == "user"), ""
        ).strip()
        if not question:
            return RagChatResponseSchema(text="질문을 입력해 주세요.")

        query_embedding = await asyncio.to_thread(generate_embedding_ollama, text=question)
        matches = await self.repository.search_similar(query_embedding, limit=_TOP_K, query_text=question)

        if not matches:
            answer = await asyncio.to_thread(
                generate_reply_ollama,
                message=(
                    "아래 질문에 답할 수 있는 업로드된 문서가 없습니다. "
                    f"문서가 없다고 한국어로 안내하세요.\n질문: {question}"
                ),
            )
            return RagChatResponseSchema(text=answer)

        context = "\n\n".join(
            f"[{m.document_name} #{m.chunk_index}]\n{m.content}" for m in matches
        )
        prompt = f"""당신은 업로드된 문서를 기반으로 답변하는 RAG 어시스턴트입니다.
아래 절차를 반드시 따르세요.

1. 사용자 질문에서 핵심 검색어(이름, 별명, 코드 등)를 뽑는다.
2. 문서 발췌의 각 행을 훑으며, 그 검색어가 "부분 문자열"로라도 포함된 값이 있는지 확인한다.
   예: 검색어가 "홍길동"이고 어떤 행의 nickname 값이 "꼬마홍길동"이라면, 이것은 일치로 간주한다.
3. 부분 일치를 찾았다면 "정확히 같은 값은 아니지만, ~에 해당하는 정보가 있습니다"라고
   그 행의 내용을 인용해 답한다. 완전히 무관해서 아무 행도 안 걸리는 경우에만 모른다고 답한다.

=== 문서 발췌 ===
{context}

=== 사용자 질문 ===
{question}"""

        answer = await asyncio.to_thread(generate_reply_ollama, message=prompt)
        return RagChatResponseSchema(text=answer)
