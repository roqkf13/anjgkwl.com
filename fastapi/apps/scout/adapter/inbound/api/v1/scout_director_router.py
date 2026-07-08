import logging

from fastapi import APIRouter

from scout.adapter.inbound.api.schemas.scout_director_schema import (
    ScoutDirectorStatusSchema,
)

logger = logging.getLogger(__name__)

scout_director_router = APIRouter(prefix="/scout", tags=["scout"])


@scout_director_router.get("/status", response_model=ScoutDirectorStatusSchema)
async def get_scout_status() -> ScoutDirectorStatusSchema:
    logger.info("[ScoutDirectorRouter] status")
    return ScoutDirectorStatusSchema(
        module="scout",
        message="Scout director is ready.",
    )
