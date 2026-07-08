from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from scout.adapter.inbound.api.schemas.scout_genre_schema import ScoutGenreSchema
from scout.app.ports.input.scout_genre_use_case import ScoutGenreUseCase
from scout.dependencies.scout_genre_provider import get_scout_genre_use_case

scout_genre_router = APIRouter(prefix="/scout/genres", tags=["scout"])


@scout_genre_router.get(
    "/",
    response_model=list[ScoutGenreSchema],
    response_model_by_alias=True,
)
async def list_scout_genres(
    use_case: Annotated[ScoutGenreUseCase, Depends(get_scout_genre_use_case)],
) -> list[ScoutGenreSchema]:
    return await use_case.list_genres()


@scout_genre_router.get(
    "/{slug}",
    response_model=ScoutGenreSchema,
    response_model_by_alias=True,
)
async def get_scout_genre(
    slug: str,
    use_case: Annotated[ScoutGenreUseCase, Depends(get_scout_genre_use_case)],
) -> ScoutGenreSchema:
    genre = await use_case.get_genre(slug)
    if not genre:
        raise HTTPException(status_code=404, detail="장르를 찾을 수 없습니다.")
    return genre
