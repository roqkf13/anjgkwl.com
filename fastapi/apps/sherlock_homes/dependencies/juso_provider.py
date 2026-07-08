from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from sherlock_homes.adapter.outbound.repositories.juso_repository import JusoRepository
from sherlock_homes.app.ports.input.juso_use_case import JusoUseCase
from sherlock_homes.app.ports.output.juso_port import JusoPort
from sherlock_homes.app.use_cases.juso_interactor import JusoInteractor


def get_juso_repository(db: AsyncSession = Depends(get_db)) -> JusoPort:
    return JusoRepository(session=db)


def get_juso_use_case(
    repository: JusoPort = Depends(get_juso_repository),
) -> JusoUseCase:
    return JusoInteractor(repository=repository)
