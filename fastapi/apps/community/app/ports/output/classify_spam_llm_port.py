from __future__ import annotations

from abc import ABC, abstractmethod


class ClassifySpamLlmPort(ABC):
    """스팸 분류를 위한 LLM 호출 게이트웨이."""

    @abstractmethod
    async def classify_raw(self, *, message: str, system: str) -> str:
        pass
