from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from admin.adapter.outbound.repositories.piper_handrick_ceo_repository import HandrickCeoRepository
from admin.app.ports.input.piper_handrick_ceo_use_case import HandrickCeoUseCase
from admin.app.ports.output.piper_handrick_ceo_port import HandrickCeoPort
from admin.app.use_cases.piper_handrick_ceo_interactor import HandrickCeoInteractor


def get_handrick_ceo_repository(
    db: AsyncSession = Depends(get_db),
) -> HandrickCeoPort:
    return HandrickCeoRepository(session=db)


def get_handrick_ceo_use_case(
    repository: HandrickCeoPort = Depends(get_handrick_ceo_repository),
) -> HandrickCeoUseCase:
    return HandrickCeoInteractor(repository=repository)
