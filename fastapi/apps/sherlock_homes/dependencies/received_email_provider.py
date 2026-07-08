from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db
from sherlock_homes.adapter.outbound.repositories.received_email_repository import ReceivedEmailRepository
from sherlock_homes.app.ports.input.received_email_use_case import ReceivedEmailUseCase
from sherlock_homes.app.use_cases.received_email_interactor import ReceivedEmailInteractor


def get_received_email_interactor(
    db: AsyncSession = Depends(get_db),
) -> ReceivedEmailUseCase:
    return ReceivedEmailInteractor(repo=ReceivedEmailRepository(session=db))
