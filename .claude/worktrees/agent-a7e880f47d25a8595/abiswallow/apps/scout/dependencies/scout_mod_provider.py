from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from scout.adapter.outbound.pg.scout_mod_pg_repository import ScoutModPgRepository
from scout.app.ports.output.scout_mod_db_repository import ScoutModDbRepository
from scout.app.ports.input.scout_mod_db_use_case import ScoutModDbUseCase
from scout.app.use_cases.scout_mod_db_interactor import ScoutModDbInteractor
from core.matrix.grid_oracle_database_manager import get_db


def get_scout_mod_repository(db: AsyncSession = Depends(get_db)) -> ScoutModDbRepository:
    return ScoutModPgRepository(session=db)


def get_scout_mod_use_case(
    repository: ScoutModDbRepository = Depends(get_scout_mod_repository),
) -> ScoutModDbUseCase:
    return ScoutModDbInteractor(repository=repository)
