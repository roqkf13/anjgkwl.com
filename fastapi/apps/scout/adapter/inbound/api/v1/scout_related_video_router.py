from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from scout.adapter.inbound.api.schemas.scout_related_video_schema import ScoutRelatedVideoSchema
from scout.app.ports.input.scout_related_video_use_case import ScoutRelatedVideoUseCase
from scout.dependencies.scout_related_video_provider import get_scout_related_video_use_case

scout_related_video_router = APIRouter(prefix="/scout", tags=["scout"])


@scout_related_video_router.get(
    "/games/{game_id}/videos",
    response_model=list[ScoutRelatedVideoSchema],
    response_model_by_alias=True,
)
async def list_scout_videos_by_game(
    game_id: int,
    use_case: Annotated[ScoutRelatedVideoUseCase, Depends(get_scout_related_video_use_case)],
) -> list[ScoutRelatedVideoSchema]:
    return await use_case.list_videos_by_game(game_id)
