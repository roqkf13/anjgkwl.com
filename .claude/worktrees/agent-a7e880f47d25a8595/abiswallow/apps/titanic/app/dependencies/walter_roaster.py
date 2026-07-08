"""Walter Roaster — composition root (DIP)."""

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from core.database import get_db
from titanic.adapter.outbound.pg.walter_roaster_pg_reopsitory import (
    WalterRoasterPgRepository,
)
from titanic.app.ports.input.walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.ports.output.walter_roaster_repository import WalterRoasterRepository
from titanic.app.use_cases.walter_roaster_interactor import WalterRoasterInteractor


def get_walter_roaster_use_case(
    db: AsyncSession = Depends(get_db),
) -> WalterRoasterUseCase:
    """라우터는 포트만 알고, PG 구현체 조립은 여기서만 수행."""
    repository: WalterRoasterRepository = WalterRoasterPgRepository(db)
    return WalterRoasterInteractor(repository)
