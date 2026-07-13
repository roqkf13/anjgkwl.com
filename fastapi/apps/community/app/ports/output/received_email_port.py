from abc import ABC, abstractmethod

from community.app.dtos.received_email_dto import ReceivedEmailCommand, ReceivedEmailListResult, ReceivedEmailResult


class ReceivedEmailPort(ABC):

    @abstractmethod
    async def save(self, command: ReceivedEmailCommand) -> ReceivedEmailResult: ...

    @abstractmethod
    async def list_all(self) -> ReceivedEmailListResult: ...
