from __future__ import annotations

from abc import ABC, abstractmethod

from scout.domain.entities.scout_mod_entity import ScoutModEntity


class ScoutModDbUseCase(ABC):
    @abstractmethod
    async def get_mods_by_game(self, game_id: int) -> list[ScoutModEntity]: ...

    @abstractmethod
    async def sync_mod(self, entity: ScoutModEntity) -> ScoutModEntity: ...
