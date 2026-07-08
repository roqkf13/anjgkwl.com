from __future__ import annotations

from abc import ABC, abstractmethod

from scout.domain.entities.scout_related_video_entity import ScoutRelatedVideoEntity


class ScoutRelatedVideoDbRepository(ABC):
    @abstractmethod
    async def find_by_game_id(self, game_id: int) -> list[ScoutRelatedVideoEntity]: ...

    @abstractmethod
    async def upsert(self, entity: ScoutRelatedVideoEntity) -> ScoutRelatedVideoEntity: ...
