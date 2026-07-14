from __future__ import annotations

from abc import ABC, abstractmethod

from scout.app.dtos.scout_search_entry_dto import ScoutSearchEntryDto


class ScoutSearchUseCase(ABC):
    @abstractmethod
    async def search_game(self, query: str) -> ScoutSearchEntryDto | None: ...
