from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from core.database import get_sqlmodel_session
from titanic.adapter.outbound.pg.walter_pg_reopsitory import WalterPgRepository

ruth_corset_router = APIRouter(prefix="/titanic/ruth", tags=["ruth_corset"])

_TRACKED_FIELDS = (
    "PassengerId",
    "Survived",
    "Pclass",
    "Name",
    "gender",
    "Age",
    "Sib_Sp",
    "Parch",
    "Ticket",
    "Fare",
    "Cabin",
    "Embarked",
)


@ruth_corset_router.get("/corset")
async def get_ruth_corset(db: AsyncSession = Depends(get_sqlmodel_session)):
    """루스(Ruth) — 결측·빈 값 점검(데이터 제약)."""
    rows = await WalterPgRepository(db).get_data()
    total = len(rows)
    missing: list[dict[str, object]] = []
    for field in _TRACKED_FIELDS:
        empty_count = sum(1 for row in rows if not str(row.get(field, "")).strip())
        if empty_count:
            missing.append(
                {
                    "field": field,
                    "empty_count": empty_count,
                    "empty_ratio": round(empty_count / total, 4) if total else 0.0,
                }
            )
    return {
        "total_rows": total,
        "fields_checked": len(_TRACKED_FIELDS),
        "missing_fields": missing,
        "is_tight": len(missing) == 0,
    }
