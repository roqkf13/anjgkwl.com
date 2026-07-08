from __future__ import annotations

from typing import Any

from sqlalchemy import func, select
from sqlmodel.ext.asyncio.session import AsyncSession

from friday13th.adapter.outbound.orm.user_model import Friday13thUser
from friday13th.app.ports.output.pamela_repository import PamelaRepository


class PamelaPgRepository(PamelaRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def email_exists(self, email: str) -> bool:
        result = await self._session.execute(
            select(func.count())
            .select_from(Friday13thUser)
            .where(Friday13thUser.email == email)
        )
        return result.scalar_one() > 0

    async def create_user(
        self,
        *,
        name: str,
        email: str,
        password_hash: str,
        role: str,
    ) -> dict[str, Any]:
        user = Friday13thUser(
            name=name,
            email=email,
            password_hash=password_hash,
            role=role,
        )
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
        }
