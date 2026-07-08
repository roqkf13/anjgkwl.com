from __future__ import annotations

from abc import ABC, abstractmethod

from scout.domain.entities.scout_genre_entity import ScoutGenreEntity


class ScoutGenreDbRepository(ABC):
    @abstractmethod
    async def find_by_slug(self, slug: str) -> ScoutGenreEntity | None: ...

    @abstractmethod
    async def find_all(self) -> list[ScoutGenreEntity]: ...

    @abstractmethod
    async def upsert(self, entity: ScoutGenreEntity) -> ScoutGenreEntity: ...
