from __future__ import annotations

import statistics
from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from core.matrix.gird_neo_theone_base import Base


# ── ORM ─────────────────────────────────────────────────────────────────────

class RoseModelOrm(Base):
    __tablename__ = "titanic_booking"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    passenger_id: Mapped[str | None] = mapped_column(String, ForeignKey("titanic_person.passenger_id"), nullable=True, unique=True)
    pclass: Mapped[str | None] = mapped_column(String, nullable=True)
    ticket: Mapped[str | None] = mapped_column(String, nullable=True)
    fare: Mapped[str | None] = mapped_column(String, nullable=True)
    cabin: Mapped[str | None] = mapped_column(String, nullable=True)
    embarked: Mapped[str | None] = mapped_column(String, nullable=True)


# ── Feature Engineering ──────────────────────────────────────────────────────

_EMBARKED_MAP: dict[str, float] = {"C": 0.0, "Q": 1.0, "S": 2.0}


def _nonempty(v: Any) -> bool:
    return v is not None and str(v).strip() != ""


def _compute_medians(records: list[dict[str, Any]]) -> tuple[float, float]:
    ages = [float(r["age"]) for r in records if _nonempty(r.get("age"))]
    fares = [float(r["fare"]) for r in records if _nonempty(r.get("fare"))]
    return (
        statistics.median(ages) if ages else 30.0,
        statistics.median(fares) if fares else 14.45,
    )


def _to_feature_vector(r: dict[str, Any], age_med: float, fare_med: float) -> list[float]:
    pclass = float(r.get("pclass") or 2)
    gender = 1.0 if (r.get("gender") or "").lower() == "male" else 0.0
    age = float(r["age"]) if _nonempty(r.get("age")) else age_med
    fare = float(r["fare"]) if _nonempty(r.get("fare")) else fare_med
    embarked = _EMBARKED_MAP.get(r.get("embarked") or "", 2.0)
    sibsp = float(r.get("sibsp") or 0)
    parch = float(r.get("parch") or 0)
    family_size = sibsp + parch + 1.0
    is_alone = 1.0 if family_size == 1.0 else 0.0
    return [pclass, gender, age, fare, embarked, family_size, is_alone]


def _build_training_set(
    records: list[dict[str, Any]],
) -> tuple[list[list[float]], list[int], float, float]:
    age_med, fare_med = _compute_medians(records)
    labeled = [r for r in records if _nonempty(r.get("survived"))]
    X = [_to_feature_vector(r, age_med, fare_med) for r in labeled]
    y = [int(r["survived"]) for r in labeled]
    return X, y, age_med, fare_med


# ── Strategy Base ────────────────────────────────────────────────────────────

class SurvivalModelStrategy(ABC):
    """생존 예측 전략 인터페이스 (sklearn 스타일)."""

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @abstractmethod
    def fit(self, X: list[list[float]], y: list[int]) -> None:
        pass

    @abstractmethod
    def predict(self, X: list[list[float]]) -> list[int]:
        pass

    @abstractmethod
    def predict_proba(self, X: list[list[float]]) -> list[float]:
        """클래스 1(생존) 확률만 반환한다."""
        pass


# ── Concrete Strategies ──────────────────────────────────────────────────────

class RandomForestStrategy(SurvivalModelStrategy):
    def __init__(self, n_estimators: int = 100) -> None:
        from sklearn.ensemble import RandomForestClassifier
        self._model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)

    @property
    def name(self) -> str:
        return "random_forest"

    @property
    def description(self) -> str:
        return "배깅 앙상블. 튜닝 없이도 안정적인 baseline."

    def fit(self, X, y) -> None:
        self._model.fit(X, y)

    def predict(self, X) -> list[int]:
        return self._model.predict(X).tolist()

    def predict_proba(self, X) -> list[float]:
        return self._model.predict_proba(X)[:, 1].tolist()


class LogisticRegressionStrategy(SurvivalModelStrategy):
    def __init__(self) -> None:
        from sklearn.linear_model import LogisticRegression
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler
        self._model = Pipeline([("scaler", StandardScaler()), ("clf", LogisticRegression(max_iter=1000, random_state=42))])

    @property
    def name(self) -> str:
        return "logistic_regression"

    @property
    def description(self) -> str:
        return "이진 분류 baseline. 아웃라이어에 강함 (표준화 포함)."

    def fit(self, X, y) -> None:
        self._model.fit(X, y)

    def predict(self, X) -> list[int]:
        return self._model.predict(X).tolist()

    def predict_proba(self, X) -> list[float]:
        return self._model.predict_proba(X)[:, 1].tolist()


class DecisionTreeStrategy(SurvivalModelStrategy):
    def __init__(self) -> None:
        from sklearn.tree import DecisionTreeClassifier
        self._model = DecisionTreeClassifier(max_depth=5, random_state=42)

    @property
    def name(self) -> str:
        return "decision_tree"

    @property
    def description(self) -> str:
        return "규칙 기반. 흐름 시각화 용이."

    def fit(self, X, y) -> None:
        self._model.fit(X, y)

    def predict(self, X) -> list[int]:
        return self._model.predict(X).tolist()

    def predict_proba(self, X) -> list[float]:
        return self._model.predict_proba(X)[:, 1].tolist()


class KNNStrategy(SurvivalModelStrategy):
    def __init__(self, n_neighbors: int = 5) -> None:
        from sklearn.neighbors import KNeighborsClassifier
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler
        self._model = Pipeline([("scaler", StandardScaler()), ("clf", KNeighborsClassifier(n_neighbors=n_neighbors))])

    @property
    def name(self) -> str:
        return "knn"

    @property
    def description(self) -> str:
        return "승객 유사도 기반. 직관적 결과 (표준화 포함)."

    def fit(self, X, y) -> None:
        self._model.fit(X, y)

    def predict(self, X) -> list[int]:
        return self._model.predict(X).tolist()

    def predict_proba(self, X) -> list[float]:
        return self._model.predict_proba(X)[:, 1].tolist()


class SVMStrategy(SurvivalModelStrategy):
    def __init__(self) -> None:
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler
        from sklearn.svm import SVC
        self._model = Pipeline([("scaler", StandardScaler()), ("clf", SVC(probability=True, random_state=42))])

    @property
    def name(self) -> str:
        return "svm"

    @property
    def description(self) -> str:
        return "초평면 기반 분류. 고차원에 강함 (표준화 포함)."

    def fit(self, X, y) -> None:
        self._model.fit(X, y)

    def predict(self, X) -> list[int]:
        return self._model.predict(X).tolist()

    def predict_proba(self, X) -> list[float]:
        return self._model.predict_proba(X)[:, 1].tolist()


class NaiveBayesStrategy(SurvivalModelStrategy):
    def __init__(self) -> None:
        from sklearn.naive_bayes import GaussianNB
        self._model = GaussianNB()

    @property
    def name(self) -> str:
        return "naive_bayes"

    @property
    def description(self) -> str:
        return "베이즈 정리 기반. 빠르고 단순."

    def fit(self, X, y) -> None:
        self._model.fit(X, y)

    def predict(self, X) -> list[int]:
        return self._model.predict(X).tolist()

    def predict_proba(self, X) -> list[float]:
        return self._model.predict_proba(X)[:, 1].tolist()


class XGBoostStrategy(SurvivalModelStrategy):
    def __init__(self) -> None:
        from xgboost import XGBClassifier
        self._model = XGBClassifier(n_estimators=100, random_state=42, eval_metric="logloss", verbosity=0)

    @property
    def name(self) -> str:
        return "xgboost"

    @property
    def description(self) -> str:
        return "그래디언트 부스팅. 고성능 앙상블."

    def fit(self, X, y) -> None:
        self._model.fit(X, y)

    def predict(self, X) -> list[int]:
        return self._model.predict(X).tolist()

    def predict_proba(self, X) -> list[float]:
        return self._model.predict_proba(X)[:, 1].tolist()


class LightGBMStrategy(SurvivalModelStrategy):
    def __init__(self) -> None:
        from lightgbm import LGBMClassifier
        self._model = LGBMClassifier(n_estimators=100, random_state=42, verbosity=-1)

    @property
    def name(self) -> str:
        return "lightgbm"

    @property
    def description(self) -> str:
        return "리프 중심 트리 부스팅. 빠르고 메모리 효율적."

    def fit(self, X, y) -> None:
        self._model.fit(X, y)

    def predict(self, X) -> list[int]:
        return self._model.predict(X).tolist()

    def predict_proba(self, X) -> list[float]:
        return self._model.predict_proba(X)[:, 1].tolist()


class CatBoostStrategy(SurvivalModelStrategy):
    def __init__(self) -> None:
        from catboost import CatBoostClassifier
        self._model = CatBoostClassifier(iterations=100, random_seed=42, verbose=0)

    @property
    def name(self) -> str:
        return "catboost"

    @property
    def description(self) -> str:
        return "범주형 피처 특화 부스팅."

    def fit(self, X, y) -> None:
        self._model.fit(X, y)

    def predict(self, X) -> list[int]:
        return self._model.predict(X).tolist()

    def predict_proba(self, X) -> list[float]:
        return self._model.predict_proba(X)[:, 1].tolist()


class PCAKMeansStrategy(SurvivalModelStrategy):
    def __init__(self, n_components: int = 2, n_clusters: int = 2) -> None:
        from sklearn.cluster import KMeans
        from sklearn.decomposition import PCA
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler
        self._pca_pipeline = Pipeline([("scaler", StandardScaler()), ("pca", PCA(n_components=n_components))])
        self._kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        self._cluster_to_label: dict[int, int] = {}

    @property
    def name(self) -> str:
        return "pca_kmeans"

    @property
    def description(self) -> str:
        return "PCA 차원 축소 + KMeans 군집. 비지도 기반 분류."

    def fit(self, X, y) -> None:
        X_pca = self._pca_pipeline.fit_transform(X)
        self._kmeans.fit(X_pca)
        labels = self._kmeans.labels_
        for cluster in range(self._kmeans.n_clusters):
            mask = [i for i, c in enumerate(labels) if c == cluster]
            survived_count = sum(y[i] for i in mask)
            self._cluster_to_label[cluster] = 1 if survived_count > len(mask) / 2 else 0

    def predict(self, X) -> list[int]:
        X_pca = self._pca_pipeline.transform(X)
        clusters = self._kmeans.predict(X_pca)
        return [self._cluster_to_label.get(int(c), 0) for c in clusters]

    def predict_proba(self, X) -> list[float]:
        return [float(p) for p in self.predict(X)]
