from __future__ import annotations

from login.app.ports.input.pamela_use_case import PamelaUseCase
from login.app.ports.output.pamela_repository import PamelaRepository
from login.app.security.password import hash_password


class SignupValidationError(Exception):
    """회원가입 입력 검증 실패."""


class DuplicateEmailError(Exception):
    """이미 등록된 이메일."""


class PamelaCommandInteractor(PamelaUseCase):
    def __init__(self, repository: PamelaRepository) -> None:
        self._repository = repository

    async def signup(
        self,
        *,
        name: str,
        email: str,
        password: str,
        password_confirm: str,
        role: str,
    ) -> dict[str, object]:
        if password != password_confirm:
            raise SignupValidationError("비밀번호가 일치하지 않습니다.")
        if len(password) < 8:
            raise SignupValidationError("비밀번호는 8자 이상이어야 합니다.")

        normalized_email = email.strip().lower()
        normalized_role = (role or "user").strip() or "user"

        if await self._repository.email_exists(normalized_email):
            raise DuplicateEmailError("이미 사용 중인 이메일입니다.")

        user = await self._repository.create_user(
            name=name.strip(),
            email=normalized_email,
            password_hash=hash_password(password),
            role=normalized_role,
        )
        return {
            "message": "회원가입이 완료되었습니다.",
            "user": user,
        }
