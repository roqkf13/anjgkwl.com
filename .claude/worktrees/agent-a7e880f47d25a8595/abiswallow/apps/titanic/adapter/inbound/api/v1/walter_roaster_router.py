import logging

from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.walter_roaster_schema import WalterRoasterSchema
from titanic.app.dependencies.walter_roaster import get_walter_roaster_use_case
from titanic.app.ports.input.walter_roaster_use_case import WalterRoasterUseCase

logger = logging.getLogger(__name__)
walter_roaster_router = APIRouter(prefix="/titanic/walter", tags=["walter"])


@walter_roaster_router.get("/myself")
async def introduce_myself(
    use_case: WalterRoasterUseCase = Depends(get_walter_roaster_use_case),
) -> WalterRoasterSchema:
    


    return await use_case.introduce_myself(
        WalterRoasterSchema(
            id=2,
            name="Walter Nicholas",
            memo="타이타닉의 일등 항해사, 승객 명단 관리 담당.",
        )
    )