from __future__ import annotations

from abc import ABC, abstractmethod

from pandas import DataFrame

from titanic.adapter.inbound.api.schemas.crew_hartley_violin_schema import HartleyViolinSchema
from titanic.app.dtos.crew_hartley_violin_dto import HartleyViolinResponse


class HartleyViolinUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: HartleyViolinSchema) -> HartleyViolinResponse:
        '''하틀리 바이올린의 자기소개 메소드'''
        pass

    @abstractmethod
    def generate_survival_charts(self, df: DataFrame) -> bytes:
        '''성별·등급·나이대별 생존율 차트를 PNG 바이트로 반환'''
        pass

    @abstractmethod
    def generate_fare_distribution(self, df: DataFrame) -> bytes:
        '''운임 분포 히스토그램 + FareBin 경계선을 PNG 바이트로 반환'''
        pass