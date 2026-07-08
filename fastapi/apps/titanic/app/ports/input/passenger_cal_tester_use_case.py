from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import CalTesterSchema
from titanic.app.dtos.passenger_cal_tester_dto import CalTesterResponse


class CalTesterUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: CalTesterSchema) -> CalTesterResponse:
        '''칼 테스터의 자기소개 메소드'''
        pass

    @abstractmethod
    def test_model(self, test_set) -> dict:
        '''walter가 가져온 test_set DataFrame으로 모델 점수를 채점하는 메소드'''
        pass

