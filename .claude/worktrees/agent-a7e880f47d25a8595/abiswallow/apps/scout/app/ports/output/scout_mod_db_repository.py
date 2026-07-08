from __future__ import annotations

from abc import ABC, abstractmethod

from scout.domain.entities.scout_mod_entity import ScoutModEntity


class ScoutModDbRepository(ABC):
    @abstractmethod
    async def find_by_game_id(self, game_id: int) -> list[ScoutModEntity]: ...

    @abstractmethod
    async def upsert(self, entity: ScoutModEntity) -> ScoutModEntity: ...
