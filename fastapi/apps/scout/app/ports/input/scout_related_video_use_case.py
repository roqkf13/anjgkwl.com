from __future__ import annotations

from abc import ABC, abstractmethod

from scout.app.dtos.scout_related_video_dto import ScoutRelatedVideoDto


class ScoutRelatedVideoUseCase(ABC):
    @abstractmethod
    async def list_videos_by_game(self, game_id: int) -> list[ScoutRelatedVideoDto]: ...
