from __future__ import annotations

from functools import lru_cache

import jwt
import redis.asyncio as redis
from fastapi import Depends, HTTPException, Request, status

from core.config import get_settings
from core.security import Role, TokenPayload, verify_token


@lru_cache
def get_redis_client() -> redis.Redis:
    settings = get_settings()
    return redis.from_url(settings.redis_url, decode_responses=True)


def _extract_token(request: Request) -> str | None:
    header = request.headers.get("authorization")
    if header and header.lower().startswith("bearer "):
        return header[7:]
    return request.cookies.get("access_token")


async def get_current_user(request: Request) -> TokenPayload:
    token = _extract_token(request)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="인증이 필요합니다.")

    settings = get_settings()
    try:
        payload = verify_token(token, aud=settings.service_aud)
    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="유효하지 않은 토큰입니다."
        ) from exc

    redis_client = get_redis_client()
    if await redis_client.exists(f"auth:blacklist:{payload.jti}"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="폐기된 토큰입니다.")

    return payload


class RoleChecker:
    def __init__(self, *allowed: Role) -> None:
        self._allowed = {role.value for role in allowed}

    def __call__(self, user: TokenPayload = Depends(get_current_user)) -> TokenPayload:
        if not self._allowed.intersection(user.roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="권한이 없습니다.")
        return user
