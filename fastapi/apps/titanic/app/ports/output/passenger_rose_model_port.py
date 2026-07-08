from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.app.dtos.passenger_rose_model_dto import RoseModelQuery, RoseModelResponse


class RoseModelPort(ABC):

    @abstractmethod
    async def introduce_myself(self, query: RoseModelQuery) -> RoseModelResponse:
        '''앤드류 설계자의 자기 소개 레포지토리 추상 메소드'''
        pass

    @abstractmethod
    async def get_all_records(self) -> list[dict[str, Any]]:
        """ML 학습에 사용할 전체 승객 데이터를 반환한다."""
        pass
