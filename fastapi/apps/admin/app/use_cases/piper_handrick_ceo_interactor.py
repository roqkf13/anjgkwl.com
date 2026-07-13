from __future__ import annotations

from admin.adapter.inbound.api.schemas.piper_handrick_ceo_schema import HandrickCeoSchema
from admin.app.dtos.piper_handrick_ceo_dto import HandrickCeoQuery, HandrickCeoResponse
from admin.app.ports.input.piper_handrick_ceo_use_case import HandrickCeoUseCase
from admin.app.ports.output.piper_handrick_ceo_port import HandrickCeoPort


class HandrickCeoInteractor(HandrickCeoUseCase):

    def __init__(self, repository: HandrickCeoPort):
        self.repository = repository

    async def introduce_myself(self, schema: HandrickCeoSchema) -> HandrickCeoResponse:
        '''리처드 헨드릭스의 자기소개 인터렉터'''
        return await self.repository.introduce_myself(HandrickCeoQuery(
            id=schema.id,
            name=schema.name,
        ))
