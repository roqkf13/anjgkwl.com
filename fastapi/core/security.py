from __future__ import annotations

import base64
import time
import uuid
from enum import Enum

import jwt
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from pydantic import BaseModel

from core.config import get_settings


class Role(str, Enum):
    """서비스 전역 역할. RBAC 판단의 최소 단위."""

    USER = "user"
    ADMIN = "admin"


class TokenPayload(BaseModel):
    sub: str
    roles: list[str]
    aud: str
    exp: int
    iat: int
    jti: str


COOKIE_KWARGS = dict(
    domain=".anjgkwl.com",
    secure=True,
    httponly=True,
    samesite="lax",
)


def _load_private_key() -> str:
    settings = get_settings()
    if not settings.jwt_private_key_b64:
        raise RuntimeError("JWT_PRIVATE_KEY_B64가 설정되지 않았습니다.")
    return base64.b64decode(settings.jwt_private_key_b64).decode("utf-8")


def _load_public_key() -> str:
    settings = get_settings()
    if not settings.jwt_public_key_b64:
        raise RuntimeError("JWT_PUBLIC_KEY_B64가 설정되지 않았습니다.")
    return base64.b64decode(settings.jwt_public_key_b64).decode("utf-8")


def create_access_token(sub: str, roles: list[str], aud: str, expires_min: int = 10) -> str:
    now = int(time.time())
    payload = {
        "sub": sub,
        "roles": roles,
        "aud": aud,
        "iat": now,
        "exp": now + expires_min * 60,
        "jti": uuid.uuid4().hex,
    }
    settings = get_settings()
    return jwt.encode(
        payload, _load_private_key(), algorithm="RS256", headers={"kid": settings.jwt_kid}
    )


def create_refresh_token(sub: str, roles: list[str] | None = None) -> str:
    now = int(time.time())
    payload = {
        "sub": sub,
        "roles": roles or [],
        "type": "refresh",
        "iat": now,
        "exp": now + 60 * 60 * 24 * 30,
        "jti": uuid.uuid4().hex,
    }
    settings = get_settings()
    return jwt.encode(
        payload, _load_private_key(), algorithm="RS256", headers={"kid": settings.jwt_kid}
    )


def verify_token(token: str, aud: str) -> TokenPayload:
    payload = jwt.decode(token, _load_public_key(), algorithms=["RS256"], audience=aud)
    return TokenPayload.model_validate(payload)


def decode_refresh_token(token: str) -> dict[str, object]:
    """리프레시 토큰 검증. access token과 달리 aud 클레임이 없어 별도로 둔다."""
    payload = jwt.decode(
        token,
        _load_public_key(),
        algorithms=["RS256"],
        options={"require": ["exp", "sub", "jti"]},
    )
    if payload.get("type") != "refresh":
        raise jwt.InvalidTokenError("refresh 토큰이 아닙니다.")
    return payload


def _int_to_base64url(value: int) -> str:
    length = (value.bit_length() + 7) // 8
    return base64.urlsafe_b64encode(value.to_bytes(length, "big")).rstrip(b"=").decode("ascii")


def get_jwks() -> dict[str, object]:
    """공개키를 JWK 형식으로 반환. 외부 검증자(다른 서비스)가 이 값으로 서명을 검증한다."""
    settings = get_settings()
    public_key = load_pem_public_key(_load_public_key().encode("utf-8"))
    if not isinstance(public_key, RSAPublicKey):
        raise RuntimeError("JWT_PUBLIC_KEY_B64는 RSA 공개키여야 합니다.")
    numbers = public_key.public_numbers()
    return {
        "keys": [
            {
                "kty": "RSA",
                "use": "sig",
                "alg": "RS256",
                "kid": settings.jwt_kid,
                "n": _int_to_base64url(numbers.n),
                "e": _int_to_base64url(numbers.e),
            }
        ]
    }
