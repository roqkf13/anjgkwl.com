from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from scout.adapter.outbound.pg.scout_game_pg_repository import ScoutGamePgRepository
from scout.app.ports.output.scout_game_db_repository import ScoutGameDbRepository
from scout.app.ports.input.scout_game_db_use_case import ScoutGameDbUseCase
from scout.app.use_cases.scout_game_db_interactor import ScoutGameDbInteractor
from core.matrix.grid_oracle_database_manager import get_db


def get_scout_game_repository(db: AsyncSession = Depends(get_db)) -> ScoutGameDbRepository:
    return ScoutGamePgRepository(session=db)


def get_scout_game_use_case(
    repository: ScoutGameDbRepository = Depends(get_scout_game_repository),
) -> ScoutGameDbUseCase:
    return ScoutGameDbInteractor(repository=repository)
