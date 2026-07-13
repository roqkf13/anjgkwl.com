from __future__ import annotations

from abc import ABC, abstractmethod

from community.app.dtos.juso_dto import ContactCommand, ContactListResult, ContactUploadResult, JusoQuery, JusoResponse


class JusoUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, query: JusoQuery) -> JusoResponse:
        pass

    @abstractmethod
    async def upload_contacts(self, commands: list[ContactCommand]) -> ContactUploadResult:
        pass

    @abstractmethod
    async def upsert_contacts(self, commands: list[ContactCommand]) -> ContactUploadResult:
        pass

    @abstractmethod
    async def list_contacts(self) -> ContactListResult:
        pass
