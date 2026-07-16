from __future__ import annotations

from abc import ABC, abstractmethod


class RagRouterClassifierPort(ABC):

    @abstractmethod
    def classify(self, text: str) -> tuple[str, float]:
        """(label, confidence)를 반환한다. label은 'rag_needed' 또는 'no_rag_needed'."""
