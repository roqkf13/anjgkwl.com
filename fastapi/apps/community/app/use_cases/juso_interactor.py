from __future__ import annotations

from community.app.dtos.juso_dto import ContactCommand, ContactListResult, ContactUploadResult, JusoQuery, JusoResponse
from community.app.ports.input.juso_use_case import JusoUseCase
from community.app.ports.output.juso_port import JusoPort


class JusoInteractor(JusoUseCase):

    def __init__(self, repository: JusoPort):
        self.repository = repository

    async def introduce_myself(self, query: JusoQuery) -> JusoResponse:
        return await self.repository.introduce_myself(query)

    async def list_contacts(self) -> ContactListResult:
        return await self.repository.list_contacts()

    async def upload_contacts(self, commands: list[ContactCommand]) -> ContactUploadResult:
        return await self.repository.save_contacts(commands)

    async def upsert_contacts(self, commands: list[ContactCommand]) -> ContactUploadResult:
        return await self.repository.upsert_contacts(commands)
