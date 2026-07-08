from __future__ import annotations

from silicon_valley.adapter.inbound.api.schemas.piper_handrick_ceo_schema import HandrickCeoSchema
from silicon_valley.app.dtos.piper_handrick_ceo_dto import HandrickCeoQuery, HandrickCeoResponse
from silicon_valley.app.ports.input.piper_handrick_ceo_use_case import HandrickCeoUseCase
from silicon_valley.app.ports.output.piper_handrick_ceo_port import HandrickCeoPort


class HandrickCeoInteractor(HandrickCeoUseCase):

    def __init__(self, repository: HandrickCeoPort):
        self.repository = repository

    async def introduce_myself(self, schema: HandrickCeoSchema) -> HandrickCeoResponse:
        '''리처드 헨드릭스의 자기소개 인터렉터'''
        return await self.repository.introduce_myself(HandrickCeoQuery(
            id=schema.id,
            name=schema.name,
        ))
