from __future__ import annotations

from silicon_valley.adapter.inbound.api.schemas.piper_gilfoyle_system_schema import GilfoyleSystemSchema
from silicon_valley.app.dtos.piper_gilfoyle_system_dto import GilfoyleSystemQuery, GilfoyleSystemResponse
from silicon_valley.app.ports.input.piper_gilfoyle_system_use_case import GilfoyleSystemUseCase
from silicon_valley.app.ports.output.piper_gilfoyle_system_port import GilfoyleSystemPort


class GilfoyleSystemInteractor(GilfoyleSystemUseCase):

    def __init__(self, repository: GilfoyleSystemPort):
        self.repository = repository

    async def introduce_myself(self, schema: GilfoyleSystemSchema) -> GilfoyleSystemResponse:
        '''버트람 길포일의 자기소개 인터렉터'''
        return await self.repository.introduce_myself(GilfoyleSystemQuery(
            id=schema.id,
            name=schema.name,
        ))
