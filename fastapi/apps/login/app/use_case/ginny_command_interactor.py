from __future__ import annotations

import secrets

from login.app.ports.input.ginny_use_case import GinnyUseCase
from login.app.ports.output.ginny_repository import GinnyRepository
from login.app.ports.output.google_oauth_port import GoogleOAuthPort

PROVIDER_GOOGLE = "google"


class GoogleOAuthError(Exception):
    """구글 로그인 처리 중 오류가 발생했을 때."""


class OAuthProfileError(Exception):
    """외부에서 전달받은 OAuth 프로필 정보가 올바르지 않을 때."""


class GinnyCommandInteractor(GinnyUseCase):
    def __init__(self, repository: GinnyRepository, oauth_client: GoogleOAuthPort) -> None:
        self._repository = repository
        self._oauth_client = oauth_client

    def build_authorize_url(self) -> tuple[str, str]:
        state = secrets.token_urlsafe(24)
        return self._oauth_client.build_authorize_url(state), state

    async def login_with_google(self, code: str) -> dict[str, object]:
        try:
            tokens = await self._oauth_client.exchange_code(code)
            userinfo = await self._oauth_client.fetch_userinfo(tokens["access_token"])
        except Exception as exc:  # noqa: BLE001 - 외부 API 실패를 단일 예외로 통일
            raise GoogleOAuthError("구글 인증에 실패했습니다.") from exc

        oauth_id = str(userinfo.get("sub") or "")
        email = str(userinfo.get("email") or "").strip().lower()
        name = str(userinfo.get("name") or email)
        if not oauth_id or not email:
            raise GoogleOAuthError("구글 계정 정보를 확인할 수 없습니다.")

        user = await self._upsert_oauth_user(
            provider=PROVIDER_GOOGLE, oauth_id=oauth_id, email=email, name=name
        )
        return {"message": "구글 로그인에 성공했습니다.", "user": user}

    async def login_with_oauth_profile(
        self, *, provider: str, oauth_id: str, email: str, name: str
    ) -> dict[str, object]:
        if not oauth_id or not email:
            raise OAuthProfileError("OAuth 계정 정보를 확인할 수 없습니다.")

        user = await self._upsert_oauth_user(
            provider=provider, oauth_id=oauth_id, email=email, name=name
        )
        return {"message": "로그인에 성공했습니다.", "user": user}

    async def _upsert_oauth_user(
        self, *, provider: str, oauth_id: str, email: str, name: str
    ) -> dict[str, object]:
        user = await self._repository.find_by_provider_id(provider, oauth_id)
        if user is None:
            user = await self._repository.find_by_email(email)
        if user is None:
            user = await self._repository.create_oauth_user(
                name=name,
                email=email,
                provider=provider,
                oauth_id=oauth_id,
                role="user",
            )

        return {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
        }
