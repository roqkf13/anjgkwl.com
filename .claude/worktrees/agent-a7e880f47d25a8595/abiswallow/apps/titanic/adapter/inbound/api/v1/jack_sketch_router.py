from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from core.database import get_sqlmodel_session

from titanic.app.ports.input.walter_use_case import WalterUseCase

from titanic.app.use_cases.walter_query import WalterQuery

jack_sketch_router = APIRouter(prefix="/titanic/jack", tags=["jack_sketch"])


def _walter_use_case(db: AsyncSession) -> WalterUseCase:
    repository: WalterRepository = WalterPgRepository(db)
    return WalterQuery(repository)


@jack_sketch_router.get("/sketch")
async def get_jack_sketch(
    db: AsyncSession = Depends(get_sqlmodel_session),
    limit: int = Query(default=10, ge=1, le=100),
):
    """잭(Jack) — 데이터 미리보기(스케치) 샘플."""
    use_case = _walter_use_case(db)
    df = await use_case.get_titanic_data()
    if df.empty:
        return {"limit": limit, "count": 0, "items": []}
    sample = df.head(limit)
    return {
        "limit": limit,
        "count": len(sample),
        "items": sample.to_dict(orient="records"),
    }
