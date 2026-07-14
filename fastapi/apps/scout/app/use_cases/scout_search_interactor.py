from __future__ import annotations

import logging
import re

from scout.app.dtos.scout_search_entry_dto import ScoutSearchEntryDto, VideoLinkDto
from scout.app.ports.input.scout_search_use_case import ScoutSearchUseCase
from scout.app.ports.output.game_search_provider import GameSearchProvider
from scout.app.ports.output.scout_search_entry_db_repository import (
    ScoutSearchEntryDbRepository,
)
from scout.domain.entities.scout_search_entry_entity import ScoutSearchEntryEntity

logger = logging.getLogger(__name__)


def _normalize_query_key(query: str) -> str:
    return re.sub(r"\s+", " ", query.strip().lower())


def _to_dto(entity: ScoutSearchEntryEntity) -> ScoutSearchEntryDto:
    return ScoutSearchEntryDto(
        id=entity.id,
        query_key=entity.query_key,
        title=entity.title,
        platform=entity.platform,
        summary=entity.summary,
        official_site_url=entity.official_site_url,
        videos=[VideoLinkDto(**v) for v in entity.videos],
    )


class ScoutSearchInteractor(ScoutSearchUseCase):
    def __init__(
        self,
        repository: ScoutSearchEntryDbRepository,
        search_provider: GameSearchProvider,
    ) -> None:
        self._repository = repository
        self._search_provider = search_provider

    async def search_game(self, query: str) -> ScoutSearchEntryDto | None:
        query_key = _normalize_query_key(query)
        if not query_key:
            return None

        cached = await self._repository.find_by_query_key(query_key)
        if cached:
            logger.info("[ScoutSearchInteractor] cache hit query_key=%s", query_key)
            return _to_dto(cached)

        logger.info("[ScoutSearchInteractor] cache miss query_key=%s -> gemini", query_key)
        found = await self._search_provider.search(query)
        if not found:
            return None

        entity = ScoutSearchEntryEntity(
            id=None,
            query_key=query_key,
            title=found.title,
            platform=found.platform,
            summary=found.summary,
            official_site_url=found.official_site_url,
            videos=found.videos,
        )
        saved = await self._repository.upsert(entity)
        return _to_dto(saved)
