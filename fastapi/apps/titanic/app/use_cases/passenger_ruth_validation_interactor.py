from __future__ import annotations

from titanic.adapter.inbound.api.schemas.passenger_ruth_validation_schema import RuthValidationSchema
from titanic.app.dtos.passenger_ruth_validation_dto import RuthValidationQuery, RuthValidationResponse
from titanic.app.ports.input.passenger_ruth_validation_use_case import RuthValidationUseCase
from titanic.app.ports.output.passenger_ruth_validation_port import RuthValidationPort


class RuthValidationInteractor(RuthValidationUseCase):
    
    def __init__(self, repository: RuthValidationPort):
        self.repository = repository

    async def introduce_myself(self, schema: RuthValidationSchema) -> RuthValidationResponse:
        '''루스 밸리데이션의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(RuthValidationQuery(
            id = schema.id,
            name = schema.name
        ))

    async def list_by_pclass(self, pclass: int, page: int, page_size: int) -> dict:
        total, items = await self.repository.list_by_pclass(pclass, page, page_size)
        return {"total": total, "page": page, "page_size": page_size, "items": items}