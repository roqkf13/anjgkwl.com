from __future__ import annotations

from abc import ABC, abstractmethod

from scout.app.dtos.scout_genre_dto import ScoutGenreDto


class ScoutGenreUseCase(ABC):
    @abstractmethod
    async def list_genres(self) -> list[ScoutGenreDto]: ...

    @abstractmethod
    async def get_genre(self, slug: str) -> ScoutGenreDto | None: ...
