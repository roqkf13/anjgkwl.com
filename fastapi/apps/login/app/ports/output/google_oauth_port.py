from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class GoogleOAuthPort(ABC):
    @abstractmethod
    def build_authorize_url(self, state: str) -> str:
        """구글 OAuth 동의 화면 URL을 만듭니다."""

    @abstractmethod
    async def exchange_code(self, code: str) -> dict[str, Any]:
        """authorization code를 access token으로 교환합니다."""

    @abstractmethod
    async def fetch_userinfo(self, access_token: str) -> dict[str, Any]:
        """access token으로 구글 사용자 정보(sub, email, name)를 조회합니다."""
