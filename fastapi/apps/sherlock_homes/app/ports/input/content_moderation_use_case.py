from __future__ import annotations

from abc import ABC, abstractmethod

from sherlock_homes.app.dtos.content_moderation_dto import ContentModerationQuery, ContentModerationResult


class ContentModerationUseCase(ABC):

    @abstractmethod
    async def moderate(self, query: ContentModerationQuery) -> ContentModerationResult:
        pass
