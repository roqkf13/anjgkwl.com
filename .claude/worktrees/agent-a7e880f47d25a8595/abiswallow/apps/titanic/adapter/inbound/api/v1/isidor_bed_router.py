from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from core.database import get_sqlmodel_session
from titanic.adapter.outbound.pg.walter_pg_reopsitory import WalterPgRepository

isidor_bed_router = APIRouter(prefix="/titanic/isidor", tags=["isidor_bed"])


@isidor_bed_router.get("/bed")
async def get_isidor_bed(
    db: AsyncSession = Depends(get_sqlmodel_session),
    limit: int = Query(default=50, ge=1, le=200),
):
    """아이더(Isidor) — 객실(Cabin)이 배정된 승객."""
    rows = await WalterPgRepository(db).get_data()
    with_cabin = [row for row in rows if str(row.get("Cabin", "")).strip()]
    items = with_cabin[:limit]
    return {
        "total_with_cabin": len(with_cabin),
        "limit": limit,
        "count": len(items),
        "items": items,
    }
