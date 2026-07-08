from typing import Annotated

from fastapi import APIRouter, Depends

from scout.adapter.inbound.api.schemas.scout_genre_schema import GenreHubSchema
from scout.app.dependencies.genre_hubs import get_soulslike_use_case
from scout.app.ports.input.genre_hub_use_case import GenreHubUseCase

soulslike_router = APIRouter(prefix="/scout/soulslike", tags=["scout"])


@soulslike_router.get("/hub", response_model=GenreHubSchema)
async def get_soulslike_hub(
    use_case: Annotated[GenreHubUseCase, Depends(get_soulslike_use_case)],
) -> GenreHubSchema:
    return await use_case.get_genre_hub()
