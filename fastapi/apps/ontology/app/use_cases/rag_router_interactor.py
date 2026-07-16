from __future__ import annotations

import asyncio

from ontology.app.dtos.rag_router_dto import RouteQueryCommand, RouteQueryResponse
from ontology.app.ports.input.rag_router_use_case import RagRouterUseCase
from ontology.app.ports.output.rag_router_classifier_port import RagRouterClassifierPort

from core.matrix.vault_keymaker_secret_manager import generate_reply, is_gemini_configured
from rag.adapter.inbound.api.schemas.rag_chat_schema import RagChatSchema, RagMessageItem
from rag.app.ports.input.rag_document_use_case import RagDocumentUseCase


class RagRouterInteractor(RagRouterUseCase):
    """분류기로 질문을 4갈래(auth/crud/general_qa/rag_needed)로 판단해 라우팅한다.

    auth/crud는 LLM을 호출하지 않고 라우팅 신호만 반환한다 — 실제 처리는
    호출한 쪽(프론트엔드 또는 상위 API)이 route 값을 보고 로그인/CRUD 플로우로 이어간다.
    """

    def __init__(self, classifier: RagRouterClassifierPort, rag_use_case: RagDocumentUseCase) -> None:
        self._classifier = classifier
        self._rag_use_case = rag_use_case

    async def route(self, command: RouteQueryCommand) -> RouteQueryResponse:
        label, confidence = await asyncio.to_thread(self._classifier.classify, command.text)

        if label in ("auth", "crud"):
            return RouteQueryResponse(route=label, answer="", confidence=confidence)

        if label == "rag_needed":
            schema = RagChatSchema(messages=[RagMessageItem(role="user", text=command.text)])
            result = await self._rag_use_case.ask(schema)
            return RouteQueryResponse(route="rag", answer=result.text, confidence=confidence)

        if not is_gemini_configured():
            raise RuntimeError("GEMINI_API_KEY가 설정되지 않았습니다. backend/.env를 확인하세요.")
        answer = await asyncio.to_thread(generate_reply, message=command.text)
        return RouteQueryResponse(route="gemini", answer=answer, confidence=confidence)
