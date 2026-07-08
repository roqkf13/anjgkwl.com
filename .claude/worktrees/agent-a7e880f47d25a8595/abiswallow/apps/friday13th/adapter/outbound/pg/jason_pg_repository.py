from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from friday13th.adapter.outbound.orm.user_model import Friday13thUser
from friday13th.app.ports.output.jason_repository import JasonRepository


class JasonPgRepository(JasonRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_email(self, email: str) -> dict[str, Any] | None:
        result = await self._session.execute(
            select(Friday13thUser).where(Friday13thUser.email == email)
        )
        row = result.scalar_one_or_none()
        if row is None:
            return None
        return {
            "id": row.id,
            "name": row.name,
            "email": row.email,
            "password_hash": row.password_hash,
            "role": row.role,
        }
