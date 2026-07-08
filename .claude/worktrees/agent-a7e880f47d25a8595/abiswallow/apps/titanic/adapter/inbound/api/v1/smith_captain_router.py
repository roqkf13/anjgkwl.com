from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from core.database import get_sqlmodel_session
from titanic.adapter.outbound.pg.walter_pg_reopsitory import WalterPgRepository
from titanic.app.ports.input.walter_use_case import WalterUseCase
from titanic.app.ports.output.walter_repository import WalterRepository
from titanic.app.use_cases.walter_query import WalterQuery

smith_captain_router = APIRouter(prefix="/titanic/smith", tags=["smith_captain"])


def _walter_use_case(db: AsyncSession) -> WalterUseCase:
    repository: WalterRepository = WalterPgRepository(db)
    return WalterQuery(repository)


@smith_captain_router.get("/summary")
async def get_smith_summary(db: AsyncSession = Depends(get_sqlmodel_session)):
    """선장(Smith) — 전체 승객·생존 현황 요약."""
    use_case = _walter_use_case(db)
    total = await use_case.get_titanic_data_count()
    survived = await use_case.get_titanic_data_count_survived()
    dead = await use_case.get_titanic_data_count_dead()
    survival_rate = round(survived / total, 4) if total else 0.0
    return {
        "total": total,
        "survived": survived,
        "dead": dead,
        "survival_rate": survival_rate,
    }
