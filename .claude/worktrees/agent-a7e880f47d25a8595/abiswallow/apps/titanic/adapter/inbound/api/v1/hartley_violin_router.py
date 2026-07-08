from __future__ import annotations

from collections import defaultdict

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from core.database import get_sqlmodel_session
from titanic.adapter.outbound.pg.walter_pg_reopsitory import WalterPgRepository

hartley_violin_router = APIRouter(prefix="/titanic/hartley", tags=["hartley_violin"])


@hartley_violin_router.get("/violin")
async def get_hartley_violin(db: AsyncSession = Depends(get_sqlmodel_session)):
    """하틀리(Hartley) — 객실 등급별 생존 분포(악보)."""
    rows = await WalterPgRepository(db).get_data()
    stats: dict[str, dict[str, int]] = defaultdict(
        lambda: {"total": 0, "survived": 0, "dead": 0}
    )
    for row in rows:
        pclass = str(row.get("Pclass", "")).strip() or "unknown"
        bucket = stats[pclass]
        bucket["total"] += 1
        if str(row.get("Survived", "")).strip() == "1":
            bucket["survived"] += 1
        elif str(row.get("Survived", "")).strip() == "0":
            bucket["dead"] += 1

    by_class = []
    for pclass, bucket in sorted(stats.items(), key=lambda item: item[0]):
        total = bucket["total"]
        survived = bucket["survived"]
        by_class.append(
            {
                "pclass": pclass,
                "total": total,
                "survived": survived,
                "dead": bucket["dead"],
                "survival_rate": round(survived / total, 4) if total else 0.0,
            }
        )
    return {"by_pclass": by_class}
