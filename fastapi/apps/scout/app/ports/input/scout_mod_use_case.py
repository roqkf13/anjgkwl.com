from __future__ import annotations

from abc import ABC, abstractmethod

from scout.app.dtos.scout_mod_dto import ScoutModDto


class ScoutModUseCase(ABC):
    @abstractmethod
    async def list_mods_by_game(self, game_id: int) -> list[ScoutModDto]: ...
