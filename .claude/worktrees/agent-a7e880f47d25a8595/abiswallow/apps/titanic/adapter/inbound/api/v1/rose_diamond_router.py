from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from core.database import get_sqlmodel_session
from titanic.adapter.outbound.pg.walter_pg_reopsitory import WalterPgRepository

rose_diamond_router = APIRouter(prefix="/titanic/rose", tags=["rose_diamond"])


def _parse_fare(value: str) -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


@rose_diamond_router.get("/diamond")
async def get_rose_diamond(
    db: AsyncSession = Depends(get_sqlmodel_session),
    limit: int = Query(default=10, ge=1, le=50),
):
    """로즈(Rose) — 운임이 높은 승객(다이아몬드급) 목록."""
    rows = await WalterPgRepository(db).get_data()
    ranked = sorted(rows, key=lambda row: _parse_fare(row.get("Fare", "")), reverse=True)
    items = ranked[:limit]
    return {"limit": limit, "count": len(items), "items": items}
