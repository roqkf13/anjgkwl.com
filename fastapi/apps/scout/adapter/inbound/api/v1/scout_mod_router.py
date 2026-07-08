from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from scout.adapter.inbound.api.schemas.scout_mod_schema import ScoutModSchema
from scout.app.ports.input.scout_mod_use_case import ScoutModUseCase
from scout.dependencies.scout_mod_provider import get_scout_mod_use_case

scout_mod_router = APIRouter(prefix="/scout", tags=["scout"])


@scout_mod_router.get(
    "/games/{game_id}/mods",
    response_model=list[ScoutModSchema],
    response_model_by_alias=True,
)
async def list_scout_mods_by_game(
    game_id: int,
    use_case: Annotated[ScoutModUseCase, Depends(get_scout_mod_use_case)],
) -> list[ScoutModSchema]:
    return await use_case.list_mods_by_game(game_id)
