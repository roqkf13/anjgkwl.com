from fastapi import APIRouter, Depends

from sherlock_homes.app.dtos.telegram_dto import TelegramQuery, TelegramResponse
from sherlock_homes.app.ports.input.telegram_use_case import TelegramUseCase
from sherlock_homes.dependencies.telegram_provider import get_telegram_use_case

telegram_router = APIRouter(prefix="/telegram", tags=["telegram"])


@telegram_router.get("/myself")
async def introduce_myself(
    telegram: TelegramUseCase = Depends(get_telegram_use_case),
) -> TelegramResponse:
    return await telegram.introduce_myself(
        TelegramQuery(id=13, name="텔레그램 채널 (Telegram)")
    )
