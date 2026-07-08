from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from core.matrix.grid_oracle_database_manager import get_db as get_sqlmodel_session
from friday13th.adapter.inbound.api.schemas.jason_login_request import (
    LoginRequest,
    LoginResponse,
)
from friday13th.adapter.outbound.pg.jason_pg_repository import JasonPgRepository
from friday13th.app.ports.input.jason_use_case import JasonUseCase
from friday13th.app.ports.output.jason_repository import JasonRepository
from friday13th.app.use_case.jason_command_interactor import (
    InvalidCredentialsError,
    JasonCommandInteractor,
)

jason_router = APIRouter(tags=["jason"])


def _jason_use_case(db: AsyncSession) -> JasonUseCase:
    repository: JasonRepository = JasonPgRepository(db)
    return JasonCommandInteractor(repository)


@jason_router.post("/login", response_model=LoginResponse)
async def login(
    body: LoginRequest,
    db: AsyncSession = Depends(get_sqlmodel_session),
) -> LoginResponse:
    use_case = _jason_use_case(db)
    try:
        result = await use_case.login(body.email, body.password)
    except InvalidCredentialsError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    return LoginResponse.model_validate(result)
