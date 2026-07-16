from __future__ import annotations

from abc import ABC, abstractmethod

from ontology.app.dtos.rag_router_dto import RouteQueryCommand, RouteQueryResponse


class RagRouterUseCase(ABC):

    @abstractmethod
    async def route(self, command: RouteQueryCommand) -> RouteQueryResponse:
        """질문을 분류해 RAG(축구 도메인) 또는 제미나이로 라우팅하고 답변까지 반환한다."""
