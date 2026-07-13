from __future__ import annotations

from abc import ABC, abstractmethod

from admin.adapter.inbound.api.schemas.piper_handrick_ceo_schema import HandrickCeoSchema
from admin.app.dtos.piper_handrick_ceo_dto import HandrickCeoResponse


class HandrickCeoUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: HandrickCeoSchema) -> HandrickCeoResponse:
        '''리처드 헨드릭스의 자기소개 메소드'''
        pass
