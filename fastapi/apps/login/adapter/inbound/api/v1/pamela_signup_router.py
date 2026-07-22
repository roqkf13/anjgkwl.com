from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db as get_sqlmodel_session
from login.adapter.inbound.api.schemas.pamela_signup_request import (
    SignupRequest,
    SignupResponse,
)
from login.adapter.outbound.pg.pamela_pg_repository import PamelaPgRepository
from login.app.ports.input.pamela_use_case import PamelaUseCase
from login.app.ports.output.pamela_repository import PamelaRepository
from login.app.use_case.pamela_command_interactor import (
    DuplicateEmailError,
    PamelaCommandInteractor,
    SignupValidationError,
)

pamela_router = APIRouter(tags=["pamela"])


def _pamela_use_case(db: AsyncSession) -> PamelaUseCase:
    repository: PamelaRepository = PamelaPgRepository(db)
    return PamelaCommandInteractor(repository)


@pamela_router.post("/signup", response_model=SignupResponse)
async def signup(
    body: SignupRequest,
    db: AsyncSession = Depends(get_sqlmodel_session),
) -> SignupResponse:
    use_case = _pamela_use_case(db)
    try:
        result = await use_case.signup(
            name=body.name,
            email=body.email,
            password=body.password,
            password_confirm=body.passwordConfirm,
            role=body.role,
        )
    except SignupValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except DuplicateEmailError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return SignupResponse.model_validate(result)
