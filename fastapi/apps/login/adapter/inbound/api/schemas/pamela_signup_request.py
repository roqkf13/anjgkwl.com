from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field, field_validator


class SignupRequest(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8)
    passwordConfirm: str = Field(min_length=8)
    role: str = Field(default="user", max_length=32)

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("이름을 입력해 주세요.")
        return stripped


class SignupUserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str


class SignupResponse(BaseModel):
    message: str
    user: SignupUserResponse
