from __future__ import annotations

from abc import ABC, abstractmethod

from scout.app.dtos.genre_hub_dto import GenreHubDto


class GenreHubRepository(ABC):
    @abstractmethod
    async def get_hub(self) -> GenreHubDto:
        ...
