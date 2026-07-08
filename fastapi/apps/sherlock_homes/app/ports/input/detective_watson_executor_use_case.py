from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_homes.app.dtos.detective_watson_executor_dto import (
    WatsonExecutorQuery,
    WatsonExecutorResponse,
    WatsonSendEmailQuery,
    WatsonSendEmailResult,
)


class WatsonExecutorUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, query: WatsonExecutorQuery) -> WatsonExecutorResponse:
        pass

    @abstractmethod
    async def send_email(self, query: WatsonSendEmailQuery) -> WatsonSendEmailResult:
        pass
