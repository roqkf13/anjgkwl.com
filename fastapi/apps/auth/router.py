from __future__ import annotations

import secrets

import jwt
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from sqlmodel.ext.asyncio.session import AsyncSession

from core.config import get_settings
from core.dependencies import get_current_user
from core.matrix.grid_oracle_database_manager import get_db as get_sqlmodel_session
from core.security import COOKIE_KWARGS, TokenPayload, get_jwks

from auth import services
from auth.schemas import LoginRequest, RefreshRequest, TokenResponse

auth_router = APIRouter(tags=["auth"])

_STATE_COOKIE = "auth_oauth_state"
_SUPPORTED_PROVIDERS = {"google", "naver"}


def _set_token_cookies(response: Response, tokens: dict[str, object]) -> None:
    response.set_cookie(
        "access_token", str(tokens["access_token"]), max_age=int(tokens["expires_in"]), **COOKIE_KWARGS
    )
    response.set_cookie(
        "refresh_token", str(tokens["refresh_token"]), max_age=60 * 60 * 24 * 30, **COOKIE_KWARGS
    )


@auth_router.post("/login", response_model=TokenResponse)
async def login(
    body: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_sqlmodel_session),
) -> TokenResponse:
    try:
        user = await services.login_with_password(db, body.email, body.password)
    except services.AuthServiceError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    tokens = await services.issue_session(user)
    _set_token_cookies(response, tokens)
    return TokenResponse.model_validate(tokens)


@auth_router.get("/login/{provider}")
async def login_with_oauth_provider(provider: str) -> RedirectResponse:
    if provider not in _SUPPORTED_PROVIDERS:
        raise HTTPException(status_code=404, detail="지원하지 않는 provider입니다.")
    state = secrets.token_urlsafe(24)
    authorize_url = services.build_provider_authorize_url(provider, state)
    response = RedirectResponse(authorize_url)
    response.set_cookie(_STATE_COOKIE, state, max_age=300, httponly=True, samesite="lax", secure=True)
    return response


@auth_router.get("/callback/{provider}")
async def oauth_callback(
    provider: str,
    request: Request,
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
    db: AsyncSession = Depends(get_sqlmodel_session),
) -> RedirectResponse:
    frontend_url = get_settings().frontend_base_url
    cookie_state = request.cookies.get(_STATE_COOKIE)

    if error or not code or not state or state != cookie_state:
        response = RedirectResponse(f"{frontend_url}/oauth-complete?oauth=error&provider={provider}")
        response.delete_cookie(_STATE_COOKIE)
        return response

    try:
        user = await services.login_with_provider(db, provider, code, state)
    except services.AuthServiceError:
        response = RedirectResponse(f"{frontend_url}/oauth-complete?oauth=error&provider={provider}")
        response.delete_cookie(_STATE_COOKIE)
        return response

    tokens = await services.issue_session(user)
    response = RedirectResponse(f"{frontend_url}/oauth-complete?oauth=success&provider={provider}")
    response.delete_cookie(_STATE_COOKIE)
    _set_token_cookies(response, tokens)
    return response


@auth_router.post("/refresh", response_model=TokenResponse)
async def refresh(
    body: RefreshRequest, request: Request, response: Response
) -> TokenResponse:
    refresh_token = body.refresh_token or request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=401, detail="refresh_token이 필요합니다.")
    try:
        tokens = await services.rotate_refresh_token(refresh_token)
    except services.AuthServiceError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=401, detail="유효하지 않은 refresh_token입니다.") from exc
    _set_token_cookies(response, tokens)
    return TokenResponse.model_validate(tokens)


@auth_router.post("/logout")
async def logout(
    response: Response, user: TokenPayload = Depends(get_current_user)
) -> dict[str, bool]:
    await services.revoke_session(user.sub)
    response.delete_cookie("access_token", domain=COOKIE_KWARGS["domain"], secure=True, samesite="lax")
    response.delete_cookie("refresh_token", domain=COOKIE_KWARGS["domain"], secure=True, samesite="lax")
    return {"ok": True}


@auth_router.get("/.well-known/jwks.json")
async def jwks() -> dict[str, object]:
    return get_jwks()
