from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from scout.adapter.outbound.gemini.gemini_game_search_provider import (
    GeminiGameSearchProvider,
)
from scout.adapter.outbound.pg.scout_search_entry_pg_repository import (
    ScoutSearchEntryPgRepository,
)
from scout.app.ports.input.scout_search_use_case import ScoutSearchUseCase
from scout.app.ports.output.game_search_provider import GameSearchProvider
from scout.app.ports.output.scout_search_entry_db_repository import (
    ScoutSearchEntryDbRepository,
)
from scout.app.use_cases.scout_search_interactor import ScoutSearchInteractor
from core.matrix.grid_oracle_database_manager import get_db


def get_scout_search_repository(
    db: AsyncSession = Depends(get_db),
) -> ScoutSearchEntryDbRepository:
    return ScoutSearchEntryPgRepository(session=db)


def get_game_search_provider() -> GameSearchProvider:
    return GeminiGameSearchProvider()


def get_scout_search_use_case(
    repository: ScoutSearchEntryDbRepository = Depends(get_scout_search_repository),
    search_provider: GameSearchProvider = Depends(get_game_search_provider),
) -> ScoutSearchUseCase:
    return ScoutSearchInteractor(repository=repository, search_provider=search_provider)
