from __future__ import annotations

from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import get_settings
from core.matrix.grid_oracle_database_manager import get_db as get_sqlmodel_session
from friday13th.adapter.outbound.google.google_oauth_client import GoogleOAuthHttpClient
from friday13th.adapter.outbound.pg.ginny_pg_repository import GinnyPgRepository
from friday13th.app.ports.input.ginny_use_case import GinnyUseCase
from friday13th.app.use_case.ginny_command_interactor import (
    GinnyCommandInteractor,
    GoogleOAuthError,
)

ginny_router = APIRouter(tags=["ginny"])

_STATE_COOKIE = "google_oauth_state"


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
