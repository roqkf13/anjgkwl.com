from __future__ import annotations

from abc import ABC, abstractmethod

from scout.app.dtos.scout_game_dto import ScoutGameDto


class ScoutGameUseCase(ABC):
    @abstractmethod
    async def get_game(self, steam_app_id: int) -> ScoutGameDto | None: ...

    @abstractmethod
    async def list_games_by_genre(self, genre_id: int) -> list[ScoutGameDto]: ...
