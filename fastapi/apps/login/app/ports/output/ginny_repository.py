from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class GinnyRepository(ABC):
    @abstractmethod
    async def find_by_provider_id(self, provider: str, oauth_id: str) -> dict[str, Any] | None:
        """provider·oauth_id로 사용자를 조회합니다. 없으면 None."""

    @abstractmethod
    async def find_by_email(self, email: str) -> dict[str, Any] | None:
        """이메일로 사용자를 조회합니다. 없으면 None."""

    @abstractmethod
    async def create_oauth_user(
        self,
        *,
        name: str,
        email: str,
        provider: str,
        oauth_id: str,
        role: str,
    ) -> dict[str, Any]:
        """소셜 로그인으로 신규 사용자를 생성합니다."""
