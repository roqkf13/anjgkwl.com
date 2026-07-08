"""Neon/PostgreSQL 연결 확인 — 라우트는 이 어댑터만 알면 된다."""

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class DatabaseHealthAdapter:
    """비동기 세션으로 DB 생존 여부를 확인한다."""

    async def check_neon_now(self, db: AsyncSession) -> dict:
        try:
            result = await db.execute(text("SELECT NOW();"))
            now = result.scalar()
            return {"status": "success", "neon_time": now}
        except Exception as e:
            return {"status": "error", "message": str(e)}


def get_db_health_adapter() -> DatabaseHealthAdapter:
    return DatabaseHealthAdapter()
