import logging

from scout.app.dtos.genre_hub_dto import GenreHubDto
from scout.app.ports.input.genre_hub_use_case import GenreHubUseCase
from scout.app.ports.output.genre_hub_repository import GenreHubRepository

logger = logging.getLogger(__name__)


class SoulslikeInteractor(GenreHubUseCase):
    def __init__(self, repository: GenreHubRepository) -> None:
        self._repository = repository

    async def get_genre_hub(self) -> GenreHubDto:
        hub = await self._repository.get_hub()
        logger.info("[SoulslikeService] get_genre_hub — id=%s", hub.id)
        return hub
