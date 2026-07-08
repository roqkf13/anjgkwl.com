from fastapi import APIRouter, Depends

from sherlock_homes.app.dtos.discord_dto import DiscordQuery, DiscordResponse
from sherlock_homes.app.ports.input.discord_use_case import DiscordUseCase
from sherlock_homes.dependencies.discord_provider import get_discord_use_case

discord_router = APIRouter(prefix="/discord", tags=["discord"])


@discord_router.get("/myself")
async def introduce_myself(
    discord: DiscordUseCase = Depends(get_discord_use_case),
) -> DiscordResponse:
    return await discord.introduce_myself(
        DiscordQuery(id=15, name="디스코드 채널 (Discord)")
    )
