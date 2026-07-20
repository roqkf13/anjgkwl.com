from __future__ import annotations

from typing import Any

from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession

from friday13th.adapter.outbound.orm.user_model import Friday13thUser
from friday13th.app.ports.output.ginny_repository import GinnyRepository


def _to_dict(row: Friday13thUser) -> dict[str, Any]:
    return {
        "id": row.id,
        "name": row.name,
        "email": row.email,
        "role": row.role,
        "provider": row.provider,
        "oauth_id": row.oauth_id,
    }


class GinnyPgRepository(GinnyRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def find_by_provider_id(self, provider: str, oauth_id: str) -> dict[str, Any] | None:
        result = await self._session.execute(
            select(Friday13thUser).where(
                Friday13thUser.provider == provider,
                Friday13thUser.oauth_id == oauth_id,
            )
        )
        row = result.scalar_one_or_none()
        return None if row is None else _to_dict(row)

    async def find_by_email(self, email: str) -> dict[str, Any] | None:
        result = await self._session.execute(
            select(Friday13thUser).where(Friday13thUser.email == email)
        )
        row = result.scalar_one_or_none()
        return None if row is None else _to_dict(row)

    async def create_oauth_user(
        self,
        *,
        name: str,
        email: str,
        provider: str,
        oauth_id: str,
        role: str,
    ) -> dict[str, Any]:
        user = Friday13thUser(
            name=name,
            email=email,
            password_hash=None,
            role=role,
            provider=provider,
            oauth_id=oauth_id,
        )
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return _to_dict(user)
