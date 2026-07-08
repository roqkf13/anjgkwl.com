from __future__ import annotations

from abc import ABC, abstractmethod

from scout.app.dtos.genre_hub_dto import GenreHubDto


class GenreHubUseCase(ABC):
    @abstractmethod
    async def get_genre_hub(self) -> GenreHubDto:
        ...
