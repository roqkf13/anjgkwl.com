from __future__ import annotations

from abc import ABC, abstractmethod

from admin.adapter.inbound.api.schemas.piper_bighetti_hr_schema import BighettiHrSchema
from admin.app.dtos.piper_bighetti_hr_dto import BighettiHrResponse


class BighettiHrUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: BighettiHrSchema) -> BighettiHrResponse:
        '''넬슨 비게티의 자기소개 메소드'''
        pass
