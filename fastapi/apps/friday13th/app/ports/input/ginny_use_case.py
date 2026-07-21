from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class GinnyUseCase(ABC):
    @abstractmethod
    def build_authorize_url(self) -> tuple[str, str]:
        """(구글 인증 URL, CSRF 방지용 state) 튜플을 만듭니다."""

    @abstractmethod
    async def login_with_google(self, code: str) -> dict[str, Any]:
        """구글 authorization code로 로그인(없으면 가입)합니다."""

    @abstractmethod
    async def login_with_oauth_profile(
        self, *, provider: str, oauth_id: str, email: str, name: str
    ) -> dict[str, Any]:
        """이미 검증된 외부 OAuth 프로필로 로그인(없으면 가입)합니다."""

    @abstractmethod
    async def find_oauth_user(
        self, *, provider: str, oauth_id: str, email: str
    ) -> dict[str, Any] | None:
        """계정을 생성하지 않고 기존 유저 존재 여부만 조회합니다."""
