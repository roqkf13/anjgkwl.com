from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from scout.adapter.outbound.pg.scout_related_video_pg_repository import ScoutRelatedVideoPgRepository
from scout.app.ports.output.scout_related_video_db_repository import ScoutRelatedVideoDbRepository
from scout.app.ports.input.scout_related_video_use_case import ScoutRelatedVideoUseCase
from scout.app.use_cases.scout_related_video_interactor import ScoutRelatedVideoInteractor
from core.matrix.grid_oracle_database_manager import get_db


def get_scout_related_video_repository(db: AsyncSession = Depends(get_db)) -> ScoutRelatedVideoDbRepository:
    return ScoutRelatedVideoPgRepository(session=db)


def get_scout_related_video_use_case(
    repository: ScoutRelatedVideoDbRepository = Depends(get_scout_related_video_repository),
) -> ScoutRelatedVideoUseCase:
    return ScoutRelatedVideoInteractor(repository=repository)
