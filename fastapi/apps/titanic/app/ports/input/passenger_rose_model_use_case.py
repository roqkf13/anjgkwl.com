from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.adapter.inbound.api.schemas.passenger_rose_model_schema import RoseModelSchema
from titanic.app.dtos.passenger_rose_model_dto import RoseModelResponse



class RoseModelUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: RoseModelSchema) -> RoseModelResponse:
        pass

    @abstractmethod
    async def analyze_rose_survival(self) -> dict[str, Any]:
        pass

    @abstractmethod
    async def predict_survival(self, passenger_data: dict[str, Any]) -> dict[str, Any]:
        pass
