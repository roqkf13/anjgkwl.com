from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from scout.adapter.inbound.api.schemas.game_detail_schema import (
    GameDetailSchema,
    PatchNoteSchema,
)
from scout.app.dependencies.game_detail import get_game_detail_use_case
from scout.app.ports.input.game_detail_use_case import GameDetailUseCase

game_detail_router = APIRouter(prefix="/scout/games", tags=["scout"])


@game_detail_router.get(
    "/{steam_app_id}/detail",
    response_model=GameDetailSchema,
    response_model_by_alias=True,
)
async def get_scout_game_detail(
    steam_app_id: int,
    use_case: Annotated[GameDetailUseCase, Depends(get_game_detail_use_case)],
) -> GameDetailSchema:
    detail = await use_case.get_game_detail(steam_app_id)
    if not detail:
        raise HTTPException(status_code=404, detail="게임을 찾을 수 없습니다.")
    return detail


@game_detail_router.get(
    "/{steam_app_id}/patch-notes/{note_id}/korean",
    response_model=PatchNoteSchema,
    response_model_by_alias=True,
)
async def get_scout_patch_note_korean(
    steam_app_id: int,
    note_id: str,
    use_case: Annotated[GameDetailUseCase, Depends(get_game_detail_use_case)],
) -> PatchNoteSchema:
    note = await use_case.translate_patch_note(steam_app_id, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="패치 노트를 찾을 수 없습니다.")
    return note
