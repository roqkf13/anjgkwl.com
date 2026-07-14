import logging
from typing import Annotated

from fastapi import APIRouter, Body, Depends

from rag.adapter.inbound.api.schemas.rag_chat_schema import RagChatResponseSchema, RagChatSchema
from rag.app.ports.input.rag_document_use_case import RagDocumentUseCase
from rag.dependencies.rag_document_provider import get_rag_document_use_case

logger = logging.getLogger(__name__)

rag_chat_router = APIRouter(tags=["rag"])


@rag_chat_router.post("/chat", response_model=RagChatResponseSchema)
async def chat(
    schema: Annotated[RagChatSchema, Body()],
    use_case: RagDocumentUseCase = Depends(get_rag_document_use_case),
) -> RagChatResponseSchema:
    for msg in schema.messages:
        logger.info("[rag/chat] messages | role=%s | text=%s", msg.role, msg.text)
    return await use_case.ask(schema)
