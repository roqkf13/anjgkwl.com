from __future__ import annotations

from abc import ABC, abstractmethod

from scout.domain.entities.scout_genre_entity import ScoutGenreEntity


class ScoutGenreDbUseCase(ABC):
    @abstractmethod
    async def get_all_genres(self) -> list[ScoutGenreEntity]: ...

    @abstractmethod
    async def sync_genre(self, entity: ScoutGenreEntity) -> ScoutGenreEntity: ...
