from __future__ import annotations

import logging
from typing import Any

import numpy as np
import pandas as pd

from titanic.adapter.inbound.api.schemas.passenger_jack_trainer_schema import JackTrainerSchema
from titanic.app.dtos.passenger_jack_trainer_dto import JackTrainerQuery, JackTrainerResponse
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.output.passenger_jack_trainer_port import JackTrainerPort
from titanic.adapter.outbound.orm.passenger_rose_model_strategies import (
    DecisionTreeStrategy,
    KNNStrategy,
    LogisticRegressionStrategy,
    RandomForestStrategy,
)


def build_all_strategies() -> dict:
    return {
        "random_forest": RandomForestStrategy,
        "logistic_regression": LogisticRegressionStrategy,
        "decision_tree": DecisionTreeStrategy,
        "knn": KNNStrategy,
    }

logger = logging.getLogger(__name__)


class JackTrainerInteractor:

    def __init__(self, repository: JackTrainerPort):
        self.repository = repository
        self._trained_strategies: dict = {}

    def train_model(self, train_set: pd.DataFrame) -> dict[str, Any]:
        '''로즈가 제안한 모델들을 훈련시키는 메소드'''
        logger.info("[JackTrainerInteractor] 학습 파이프라인 시작")



        X_train: list[list[float]] = train.values.tolist()

        # 8. 로즈의 10개 전략으로 학습
        self._trained_strategies = {}
        trained_names = []
        for key, StrategyClass in build_all_strategies().items():
            strategy = StrategyClass()
            try:
                strategy.fit(X_train, y_label)
                self._trained_strategies[key] = strategy
                trained_names.append(strategy.name)
                logger.info(f"[JackTrainerInteractor] {strategy.name} 학습 완료")
            except Exception as e:
                logger.warning(f"[JackTrainerInteractor] {key} 학습 실패 | error={e}")

        return {
            "train_samples": len(X_train),
            "trained_models": trained_names,
            "trained_strategies": self._trained_strategies,  # CalTesterInteractor에 전달
        }


    async def introduce_myself(self, schema: JackTrainerSchema) -> JackTrainerResponse:
        '''잭 트레이너의 자기소개 메소드'''
        query = JackTrainerQuery(id=schema.id, name=schema.name)
        return await self.repository.introduce_myself(query)