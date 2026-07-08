from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_homes.app.dtos.classify_spam_dto import ClassifySpamQuery, ClassifySpamResult


class ClassifySpamUseCase(ABC):

    @abstractmethod
    async def classify(self, query: ClassifySpamQuery) -> ClassifySpamResult:
        """이메일 제목·본문을 받아 스팸 카테고리를 반환한다."""
        pass
