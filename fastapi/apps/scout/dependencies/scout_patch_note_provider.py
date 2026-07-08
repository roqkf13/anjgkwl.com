from __future__ import annotations

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from scout.adapter.outbound.pg.scout_patch_note_pg_repository import ScoutPatchNotePgRepository
from scout.app.ports.output.scout_patch_note_db_repository import ScoutPatchNoteDbRepository
from scout.app.ports.input.scout_patch_note_use_case import ScoutPatchNoteUseCase
from scout.app.use_cases.scout_patch_note_interactor import ScoutPatchNoteInteractor
from core.matrix.grid_oracle_database_manager import get_db


def get_scout_patch_note_repository(db: AsyncSession = Depends(get_db)) -> ScoutPatchNoteDbRepository:
    return ScoutPatchNotePgRepository(session=db)


def get_scout_patch_note_use_case(
    repository: ScoutPatchNoteDbRepository = Depends(get_scout_patch_note_repository),
) -> ScoutPatchNoteUseCase:
    return ScoutPatchNoteInteractor(repository=repository)
