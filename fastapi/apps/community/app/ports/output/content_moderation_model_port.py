from __future__ import annotations

from abc import ABC, abstractmethod


class ContentModerationModelPort(ABC):
    """텍스트를 분류해 (최고 점수 라벨, 점수)를 반환하는 욕설/혐오표현 판별 모델."""

    @abstractmethod
    def classify(self, text: str) -> tuple[str, float]:
        pass
