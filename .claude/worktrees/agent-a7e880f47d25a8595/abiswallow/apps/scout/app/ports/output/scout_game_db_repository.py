from __future__ import annotations

from abc import ABC, abstractmethod

from scout.domain.entities.scout_game_entity import ScoutGameEntity


class ScoutGameDbRepository(ABC):
    @abstractmethod
    async def find_by_steam_app_id(self, steam_app_id: int) -> ScoutGameEntity | None: ...

    @abstractmethod
    async def find_by_genre_id(self, genre_id: int) -> list[ScoutGameEntity]: ...

    @abstractmethod
    async def upsert(self, entity: ScoutGameEntity) -> ScoutGameEntity: ...
