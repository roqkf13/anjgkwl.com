from __future__ import annotations

import logging
import statistics
from typing import Any

from titanic.adapter.inbound.api.schemas.passenger_cal_tester_schema import CalTesterSchema
from titanic.app.dtos.passenger_cal_tester_dto import CalTesterQuery, CalTesterResponse
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.app.ports.output.passenger_cal_tester_port import CalTesterPort
from titanic.adapter.outbound.orm.passenger_rose_model_strategies import (
    DecisionTreeStrategy,
    KNNStrategy,
    LogisticRegressionStrategy,
    RandomForestStrategy,
    SurvivalModelStrategy,
    _build_training_set,
)

logger = logging.getLogger(__name__)


def _cross_validate(
    strategy_cls: type[SurvivalModelStrategy],
    X: list[list[float]],
    y: list[int],
    n_splits: int = 5,
) -> list[float]:
    """StratifiedKFold n_splits번 학습·평가 후 각 폴드 정확도를 반환한다."""
    from sklearn.model_selection import StratifiedKFold

    kf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)
    fold_scores: list[float] = []

    for train_idx, val_idx in kf.split(X, y):
        X_train = [X[i] for i in train_idx]
        y_train = [y[i] for i in train_idx]
        X_val   = [X[i] for i in val_idx]
        y_val   = [y[i] for i in val_idx]

        strategy = strategy_cls()
        strategy.fit(X_train, y_train)

        correct = sum(
            1 for i, x in enumerate(X_val)
            if strategy.predict(x)["survived"] == y_val[i]
        )
        fold_scores.append(correct / len(y_val))

    return fold_scores


class CalTesterInteractor(CalTesterUseCase):

    def __init__(self, repository: CalTesterPort) -> None:
        self.repository = repository
        self._scores: dict[str, Any] = {}

    async def introduce_myself(self, schema: CalTesterSchema) -> CalTesterResponse:
        '''칼 테스터의 자기소개 메소드'''
        query = CalTesterQuery(id=schema.id, name=schema.name)
        return await self.repository.introduce_myself(query)

    def test_model(self, test_set) -> dict:
        """walter가 가져온 test_set DataFrame으로 모델 점수를 채점하는 메소드."""
        records = test_set.to_dict('records')
        X, y, _, _ = _build_training_set(records)

        if not X:
            self._scores = {"message": "채점할 레이블 데이터가 없습니다.", "ranking": []}
            return self._scores

        strategy_classes: list[tuple[str, type[SurvivalModelStrategy]]] = [
            ("random_forest",       RandomForestStrategy),
            ("logistic_regression", LogisticRegressionStrategy),
            ("decision_tree",       DecisionTreeStrategy),
            ("knn",                 KNNStrategy),
        ]

        scores: dict[str, Any] = {}
        for name, cls in strategy_classes:
            fold_scores = _cross_validate(cls, X, y, n_splits=5)
            mean_acc = statistics.mean(fold_scores)
            std_acc  = statistics.stdev(fold_scores)
            scores[name] = {
                "cv_mean_accuracy": round(mean_acc, 4),
                "cv_std":           round(std_acc, 4),
                "fold_scores":      [round(s, 4) for s in fold_scores],
            }
            logger.info(f"[CalTesterInteractor] {name} | mean={mean_acc:.4f} std={std_acc:.4f}")

        ranked = sorted(
            scores.items(),
            key=lambda kv: kv[1]["cv_mean_accuracy"],
            reverse=True,
        )
        self._scores = {
            "ranking": [
                {"rank": i + 1, "model": name, **info}
                for i, (name, info) in enumerate(ranked)
            ],
            "sample_count": len(X),
            "cv_folds": 5,
        }
        return self._scores

    def get_latest_scores(self) -> dict[str, Any]:
        """마지막 채점 결과를 반환한다. test_model 선호출 필요."""
        return self._scores
