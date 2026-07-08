from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_homes.app.dtos.detective_watson_executor_dto import WatsonSendEmailQuery, WatsonSendEmailResult


class WatsonEmailGatewayPort(ABC):

    @abstractmethod
    async def send_email(self, query: WatsonSendEmailQuery, *, subject: str, body: str) -> WatsonSendEmailResult:
        pass
