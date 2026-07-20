from __future__ import annotations

from friday13th.app.ports.input.jason_use_case import JasonUseCase
from friday13th.app.ports.output.jason_repository import JasonRepository
from friday13th.app.security.password import verify_password


class InvalidCredentialsError(Exception):
    """이메일 또는 비밀번호가 올바르지 않을 때."""


class JasonCommandInteractor(JasonUseCase):
    def __init__(self, repository: JasonRepository) -> None:
        self._repository = repository

    async def login(self, email: str, password: str) -> dict[str, object]:
        normalized_email = email.strip().lower()
        user = await self._repository.find_by_email(normalized_email)
        if user is None:
            raise InvalidCredentialsError("이메일 또는 비밀번호가 올바르지 않습니다.")

        if user["password_hash"] is None or not verify_password(
            password, user["password_hash"]
        ):
            raise InvalidCredentialsError("이메일 또는 비밀번호가 올바르지 않습니다.")

        return {
            "message": "로그인에 성공했습니다.",
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"],
            },
        }
