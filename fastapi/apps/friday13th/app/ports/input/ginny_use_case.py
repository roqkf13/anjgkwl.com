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
