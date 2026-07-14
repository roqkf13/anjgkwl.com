from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query

from scout.adapter.inbound.api.schemas.scout_search_entry_schema import (
    ScoutSearchEntrySchema,
)
from scout.app.ports.input.scout_search_use_case import ScoutSearchUseCase
from scout.dependencies.scout_search_provider import get_scout_search_use_case

scout_search_router = APIRouter(prefix="/scout/search", tags=["scout"])


@scout_search_router.get(
    "",
    response_model=ScoutSearchEntrySchema,
    response_model_by_alias=True,
)
async def search_game(
    use_case: Annotated[ScoutSearchUseCase, Depends(get_scout_search_use_case)],
    q: str = Query(..., min_length=1),
) -> ScoutSearchEntrySchema:
    if not q.strip():
        raise HTTPException(status_code=400, detail="검색어를 입력하세요.")

    result = await use_case.search_game(q)
    if not result:
        raise HTTPException(status_code=404, detail="게임 정보를 찾을 수 없습니다.")
    return result
