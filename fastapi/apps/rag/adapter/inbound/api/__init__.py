from fastapi import APIRouter

from rag.adapter.inbound.api.v1.rag_chat_router import rag_chat_router
from rag.adapter.inbound.api.v1.rag_document_router import rag_document_router

rag_router = APIRouter(prefix="/rag", tags=["rag"])
rag_router.include_router(rag_document_router)
rag_router.include_router(rag_chat_router)
