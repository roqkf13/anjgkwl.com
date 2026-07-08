from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.app.dtos.passenger_cal_tester_dto import CalTesterQuery, CalTesterResponse


class CalTesterPort(ABC):

    @abstractmethod
    async def introduce_myself(self, query: CalTesterQuery) -> CalTesterResponse:
        '''칼 테스터의 자기 소개 레포지토리 추상 메소드'''
        pass

    @abstractmethod
    async def get_scoring_data(self) -> list[dict[str, Any]]:
        """교차검증 채점에 사용할 전체 승객 피처 데이터를 반환한다."""
        pass
