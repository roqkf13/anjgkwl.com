from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from scout.adapter.inbound.api.schemas.scout_game_schema import ScoutGameSchema
from scout.app.ports.input.scout_game_use_case import ScoutGameUseCase
from scout.dependencies.scout_game_provider import get_scout_game_use_case

scout_game_router = APIRouter(prefix="/scout/games", tags=["scout"])


@scout_game_router.get(
    "/by-genre/{genre_id}",
    response_model=list[ScoutGameSchema],
    response_model_by_alias=True,
)
async def list_scout_games_by_genre(
    genre_id: int,
    use_case: Annotated[ScoutGameUseCase, Depends(get_scout_game_use_case)],
) -> list[ScoutGameSchema]:
    return await use_case.list_games_by_genre(genre_id)


@scout_game_router.get(
    "/{steam_app_id}",
    response_model=ScoutGameSchema,
    response_model_by_alias=True,
)
async def get_scout_game(
    steam_app_id: int,
    use_case: Annotated[ScoutGameUseCase, Depends(get_scout_game_use_case)],
) -> ScoutGameSchema:
    game = await use_case.get_game(steam_app_id)
    if not game:
        raise HTTPException(status_code=404, detail="게임을 찾을 수 없습니다.")
    return game
