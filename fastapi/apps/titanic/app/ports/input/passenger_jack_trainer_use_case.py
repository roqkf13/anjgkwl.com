from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerResponse


class JackTrainerUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema) -> JackTrainerResponse:
        pass

    @abstractmethod
    async def train_models(self, schema) -> JackTrainerResponse:
        '''로즈가 제안한 모델들을 훈련시키는 메소드'''

    @abstractmethod
    def train_model(self, train_set) -> dict:
        '''walter가 가져온 train_set DataFrame으로 모델들을 훈련시키는 메소드'''

    @abstractmethod
    async def analyze_jack_dawson(self) -> dict[str, Any]:
        pass

    @abstractmethod
    async def predict_survival(self, passenger_data: dict[str, Any]) -> dict[str, Any]:
        pass
