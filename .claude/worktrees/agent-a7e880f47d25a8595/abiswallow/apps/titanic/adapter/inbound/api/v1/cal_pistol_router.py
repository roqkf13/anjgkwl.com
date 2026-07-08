from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from core.database import get_sqlmodel_session
from titanic.adapter.outbound.pg.walter_pg_reopsitory import WalterPgRepository

cal_pistol_router = APIRouter(prefix="/titanic/cal", tags=["cal_pistol"])


@cal_pistol_router.get("/pistol")
async def get_cal_pistol(db: AsyncSession = Depends(get_sqlmodel_session)):
    """칼(Cal) — 1등석(Pclass=1) 승객 생존 통계."""
    rows = await WalterPgRepository(db).get_data()
    first_class = [row for row in rows if str(row.get("Pclass", "")).strip() == "1"]
    total = len(first_class)
    survived = sum(
        1 for row in first_class if str(row.get("Survived", "")).strip() == "1"
    )
    dead = sum(1 for row in first_class if str(row.get("Survived", "")).strip() == "0")
    return {
        "pclass": "1",
        "total": total,
        "survived": survived,
        "dead": dead,
        "survival_rate": round(survived / total, 4) if total else 0.0,
    }
