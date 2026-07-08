from __future__ import annotations

from abc import ABC, abstractmethod

from scout.domain.entities.scout_game_entity import ScoutGameEntity


class ScoutGameDbUseCase(ABC):
    @abstractmethod
    async def get_game_by_steam_id(self, steam_app_id: int) -> ScoutGameEntity | None: ...

    @abstractmethod
    async def sync_game(self, entity: ScoutGameEntity) -> ScoutGameEntity: ...
