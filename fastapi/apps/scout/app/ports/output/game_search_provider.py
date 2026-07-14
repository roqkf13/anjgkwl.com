from __future__ import annotations

from abc import ABC, abstractmethod

from scout.domain.entities.scout_search_entry_entity import ScoutSearchEntryEntity


class GameSearchProvider(ABC):
    @abstractmethod
    async def search(self, query: str) -> ScoutSearchEntryEntity | None: ...
