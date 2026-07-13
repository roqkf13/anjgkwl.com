from __future__ import annotations

from abc import ABC, abstractmethod

from scout.domain.entities.scout_search_entry_entity import ScoutSearchEntryEntity


class ScoutSearchEntryDbRepository(ABC):
    @abstractmethod
    async def find_by_query_key(self, query_key: str) -> ScoutSearchEntryEntity | None: ...

    @abstractmethod
    async def upsert(self, entity: ScoutSearchEntryEntity) -> ScoutSearchEntryEntity: ...
