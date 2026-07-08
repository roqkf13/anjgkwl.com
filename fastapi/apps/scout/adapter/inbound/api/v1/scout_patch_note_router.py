from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from scout.adapter.inbound.api.schemas.scout_patch_note_schema import ScoutPatchNoteSchema
from scout.app.ports.input.scout_patch_note_use_case import ScoutPatchNoteUseCase
from scout.dependencies.scout_patch_note_provider import get_scout_patch_note_use_case

scout_patch_note_router = APIRouter(prefix="/scout", tags=["scout"])


@scout_patch_note_router.get(
    "/patch-notes/{external_note_id}",
    response_model=ScoutPatchNoteSchema,
    response_model_by_alias=True,
)
async def get_scout_patch_note(
    external_note_id: str,
    use_case: Annotated[ScoutPatchNoteUseCase, Depends(get_scout_patch_note_use_case)],
) -> ScoutPatchNoteSchema:
    note = await use_case.get_patch_note(external_note_id)
    if not note:
        raise HTTPException(status_code=404, detail="패치노트를 찾을 수 없습니다.")
    return note
