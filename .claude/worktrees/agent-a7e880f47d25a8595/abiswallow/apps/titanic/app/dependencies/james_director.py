"""James Director — composition root (DIP)."""

from fastapi import Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from core.database import get_db
from titanic.adapter.outbound.pg.james_director_pg_repository import (
    JamesDirectorPgRepository,
)
from titanic.app.ports.input.james_director_use_case import JamesDirectorUseCase
from titanic.app.use_cases.james_director_interactor import JamesDirectorInteractor


def get_james_director_use_case(
    db: AsyncSession = Depends(get_db),
) -> JamesDirectorUseCase:
    """라우터는 포트만 알고, PG 구현체 조립은 여기서만 수행."""
    repository = JamesDirectorPgRepository(db)
    return JamesDirectorInteractor(repository)
