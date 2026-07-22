from __future__ import annotations

from urllib.parse import urlencode

import httpx
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import get_settings
from core.dependencies import get_redis_client
from core.security import Role, create_access_token, create_refresh_token, decode_refresh_token
from login.adapter.outbound.google.google_oauth_client import GoogleOAuthHttpClient
from login.adapter.outbound.pg.ginny_pg_repository import GinnyPgRepository
from login.adapter.outbound.pg.jason_pg_repository import JasonPgRepository
from login.app.use_case.ginny_command_interactor import (
    GinnyCommandInteractor,
    OAuthProfileError,
)
from login.app.use_case.jason_command_interactor import (
    InvalidCredentialsError,
    JasonCommandInteractor,
)

NAVER_AUTHORIZE_URL = "https://nid.naver.com/oauth2.0/authorize"
NAVER_TOKEN_URL = "https://nid.naver.com/oauth2.0/token"
NAVER_PROFILE_URL = "https://openapi.naver.com/v1/nid/me"

REFRESH_SESSION_TTL_SECONDS = 60 * 60 * 24 * 30  # 30일, create_refresh_token의 만료와 맞춤
ACCESS_TOKEN_TTL_SECONDS = 600


class AuthServiceError(Exception):
    """auth 게이트웨이 처리 중 발생하는 공통 예외."""


class NaverOAuthClient:
    """apps/login은 건드리지 않는다는 하네스 규칙 때문에, 네이버 OAuth를 여기서 독립적으로 구현한다.
    (지금까지 네이버 로그인은 Next.js에만 있었고, 파이썬 쪽엔 없었음.)
    """

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str) -> None:
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri

    def build_authorize_url(self, state: str) -> str:
        params = {
            "response_type": "code",
            "client_id": self._client_id,
            "redirect_uri": self._redirect_uri,
            "state": state,
        }
        return f"{NAVER_AUTHORIZE_URL}?{urlencode(params)}"

    async def exchange_code(self, code: str, state: str) -> dict[str, object]:
        params = {
            "grant_type": "authorization_code",
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "redirect_uri": self._redirect_uri,
            "code": code,
            "state": state,
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{NAVER_TOKEN_URL}?{urlencode(params)}")
            response.raise_for_status()
            return response.json()

    async def fetch_userinfo(self, access_token: str) -> dict[str, object]:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                NAVER_PROFILE_URL,
                headers={"Authorization": f"Bearer {access_token}"},
            )
            response.raise_for_status()
            return response.json()


def _google_client() -> GoogleOAuthHttpClient:
    settings = get_settings()
    return GoogleOAuthHttpClient(
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
        redirect_uri=settings.auth_google_redirect_uri,
    )


def _naver_client() -> NaverOAuthClient:
    settings = get_settings()
    return NaverOAuthClient(
        client_id=settings.auth_naver_client_id,
        client_secret=settings.auth_naver_client_secret,
        redirect_uri=settings.auth_naver_redirect_uri,
    )


def build_provider_authorize_url(provider: str, state: str) -> str:
    if provider == "google":
        return _google_client().build_authorize_url(state)
    if provider == "naver":
        return _naver_client().build_authorize_url(state)
    raise AuthServiceError(f"지원하지 않는 provider입니다: {provider}")


async def _find_or_create_user(
    db: AsyncSession, provider: str, oauth_id: str, email: str, name: str
) -> dict[str, object]:
    repository = GinnyPgRepository(db)
    # login_with_oauth_profile은 oauth_client를 실제로 쓰지 않지만, 기존 apps/login의
    # 생성자 시그니처를 그대로 재사용하기 위해 google client를 그대로 넘긴다.
    interactor = GinnyCommandInteractor(repository, oauth_client=_google_client())
    try:
        result = await interactor.login_with_oauth_profile(
            provider=provider, oauth_id=oauth_id, email=email, name=name
        )
    except OAuthProfileError as exc:
        raise AuthServiceError(str(exc)) from exc
    return result["user"]


async def login_with_provider(
    db: AsyncSession, provider: str, code: str, state: str
) -> dict[str, object]:
    if provider == "google":
        client = _google_client()
        tokens = await client.exchange_code(code)
        access_token = tokens.get("access_token")
        if not access_token:
            raise AuthServiceError("구글 토큰 교환에 실패했습니다.")
        userinfo = await client.fetch_userinfo(access_token)
        oauth_id = str(userinfo.get("sub") or "")
        email = str(userinfo.get("email") or "").strip().lower()
        name = str(userinfo.get("name") or email)
    elif provider == "naver":
        client = _naver_client()
        tokens = await client.exchange_code(code, state)
        access_token = tokens.get("access_token")
        if not access_token:
            raise AuthServiceError("네이버 토큰 교환에 실패했습니다.")
        profile_json = await client.fetch_userinfo(access_token)
        if profile_json.get("resultcode") != "00":
            raise AuthServiceError("네이버 프로필 조회에 실패했습니다.")
        profile = profile_json.get("response") or {}
        oauth_id = str(profile.get("id") or "")
        email = str(profile.get("email") or "").strip().lower()
        name = str(profile.get("name") or profile.get("nickname") or email)
    else:
        raise AuthServiceError(f"지원하지 않는 provider입니다: {provider}")

    if not oauth_id or not email:
        raise AuthServiceError("계정 정보를 확인할 수 없습니다.")

    return await _find_or_create_user(db, provider, oauth_id, email, name)


async def login_with_password(db: AsyncSession, email: str, password: str) -> dict[str, object]:
    repository = JasonPgRepository(db)
    interactor = JasonCommandInteractor(repository)
    try:
        result = await interactor.login(email, password)
    except InvalidCredentialsError as exc:
        raise AuthServiceError(str(exc)) from exc
    return result["user"]


async def issue_session(user: dict[str, object]) -> dict[str, object]:
    settings = get_settings()
    sub = str(user["id"])
    roles = [str(user.get("role") or Role.USER.value)]

    access_token = create_access_token(sub=sub, roles=roles, aud=settings.service_aud)
    refresh_token = create_refresh_token(sub=sub, roles=roles)
    refresh_payload = decode_refresh_token(refresh_token)

    redis_client = get_redis_client()
    session_key = f"auth:refresh:sessions:{sub}"
    await redis_client.sadd(session_key, str(refresh_payload["jti"]))
    await redis_client.expire(session_key, REFRESH_SESSION_TTL_SECONDS)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_TTL_SECONDS,
    }


async def rotate_refresh_token(refresh_token: str) -> dict[str, object]:
    payload = decode_refresh_token(refresh_token)
    sub = str(payload["sub"])
    jti = str(payload["jti"])
    roles = list(payload.get("roles") or [])

    redis_client = get_redis_client()
    session_key = f"auth:refresh:sessions:{sub}"
    is_active = await redis_client.sismember(session_key, jti)
    if not is_active:
        # 이미 사용됐거나 알 수 없는 리프레시 토큰이 재사용됨 → 탈취 의심, 세션 전체 폐기.
        await redis_client.delete(session_key)
        raise AuthServiceError("리프레시 토큰 재사용이 감지되어 세션이 폐기되었습니다.")

    await redis_client.srem(session_key, jti)

    settings = get_settings()
    new_access = create_access_token(sub=sub, roles=roles, aud=settings.service_aud)
    new_refresh = create_refresh_token(sub=sub, roles=roles)
    new_payload = decode_refresh_token(new_refresh)
    await redis_client.sadd(session_key, str(new_payload["jti"]))
    await redis_client.expire(session_key, REFRESH_SESSION_TTL_SECONDS)

    return {
        "access_token": new_access,
        "refresh_token": new_refresh,
        "token_type": "bearer",
        "expires_in": ACCESS_TOKEN_TTL_SECONDS,
    }


async def revoke_session(sub: str) -> None:
    redis_client = get_redis_client()
    await redis_client.delete(f"auth:refresh:sessions:{sub}")
