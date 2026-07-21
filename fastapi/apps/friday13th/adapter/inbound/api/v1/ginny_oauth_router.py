from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import get_settings
from core.matrix.grid_oracle_database_manager import get_db as get_sqlmodel_session
from friday13th.adapter.outbound.google.google_oauth_client import GoogleOAuthHttpClient
from friday13th.adapter.outbound.pg.ginny_pg_repository import GinnyPgRepository
from friday13th.app.ports.input.ginny_use_case import GinnyUseCase
from friday13th.app.use_case.ginny_command_interactor import (
    GinnyCommandInteractor,
    GoogleOAuthError,
    OAuthProfileError,
)

ginny_router = APIRouter(tags=["ginny"])

_STATE_COOKIE = "google_oauth_state"

# FastAPI가 직접 code를 교환하지 않는 provider(예: 네이버)는 프론트엔드(Next.js)가
# OAuth 핸드셰이크를 마친 뒤 검증된 프로필만 여기로 넘겨 유저를 업서트한다.
_EXTERNAL_UPSERT_PROVIDERS = {"naver"}


class OAuthProfilePayload(BaseModel):
    provider: str
    oauth_id: str
    email: str
    name: str


def _ginny_use_case(db: AsyncSession) -> GinnyUseCase:
    settings = get_settings()
    repository = GinnyPgRepository(db)
    oauth_client = GoogleOAuthHttpClient(
        client_id=settings.google_client_id,
        client_secret=settings.google_client_secret,
        redirect_uri=settings.google_oauth_redirect_uri,
    )
    return GinnyCommandInteractor(repository, oauth_client)


@ginny_router.get("/auth/google/login")
async def google_login(db: AsyncSession = Depends(get_sqlmodel_session)) -> RedirectResponse:
    use_case = _ginny_use_case(db)
    authorize_url, state = use_case.build_authorize_url()
    response = RedirectResponse(authorize_url)
    response.set_cookie(_STATE_COOKIE, state, max_age=300, httponly=True, samesite="lax")
    return response


@ginny_router.get("/auth/google/callback")
async def google_callback(
    request: Request,
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
    db: AsyncSession = Depends(get_sqlmodel_session),
) -> RedirectResponse:
    frontend_url = get_settings().frontend_base_url
    cookie_state = request.cookies.get(_STATE_COOKIE)

    if error or not code or not state or state != cookie_state:
        return RedirectResponse(f"{frontend_url}/login?oauth=error")

    use_case = _ginny_use_case(db)
    try:
        await use_case.login_with_google(code)
    except GoogleOAuthError:
        return RedirectResponse(f"{frontend_url}/login?oauth=error")

    response = RedirectResponse(f"{frontend_url}/login?oauth=success")
    response.delete_cookie(_STATE_COOKIE)
    return response


@ginny_router.post("/auth/oauth/upsert")
async def upsert_oauth_profile(
    payload: OAuthProfilePayload,
    request: Request,
    db: AsyncSession = Depends(get_sqlmodel_session),
) -> dict[str, object]:
    """프론트엔드(Next.js)가 자체적으로 처리한 OAuth(예: 네이버) 결과를 유저 테이블에 반영한다.

    이 엔드포인트는 브라우저가 아닌 신뢰된 서버(Next.js API route)만 호출해야 하므로
    공유 비밀값(X-Internal-Secret)으로 검증한다.
    """
    settings = get_settings()
    provided_secret = request.headers.get("x-internal-secret", "")
    if not settings.internal_oauth_secret or provided_secret != settings.internal_oauth_secret:
        raise HTTPException(status_code=401, detail="인증되지 않은 요청입니다.")
    if payload.provider not in _EXTERNAL_UPSERT_PROVIDERS:
        raise HTTPException(status_code=400, detail="지원하지 않는 provider입니다.")

    use_case = _ginny_use_case(db)
    try:
        return await use_case.login_with_oauth_profile(
            provider=payload.provider,
            oauth_id=payload.oauth_id,
            email=payload.email,
            name=payload.name,
        )
    except OAuthProfileError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
