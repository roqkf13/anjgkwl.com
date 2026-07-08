from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from scout.adapter.outbound.pg.scout_genre_pg_repository import ScoutGenrePgRepository
from scout.app.ports.output.scout_genre_db_repository import ScoutGenreDbRepository
from scout.app.ports.input.scout_genre_db_use_case import ScoutGenreDbUseCase
from scout.app.use_cases.scout_genre_db_interactor import ScoutGenreDbInteractor
from core.matrix.grid_oracle_database_manager import get_db


def get_scout_genre_repository(db: AsyncSession = Depends(get_db)) -> ScoutGenreDbRepository:
    return ScoutGenrePgRepository(session=db)


def get_scout_genre_use_case(
    repository: ScoutGenreDbRepository = Depends(get_scout_genre_repository),
) -> ScoutGenreDbUseCase:
    return ScoutGenreDbInteractor(repository=repository)
