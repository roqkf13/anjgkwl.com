from fastapi import APIRouter, Depends

from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import WalterRoasterSchema
from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterResponse
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.dependencies.crew_walter_roaster_provider import get_walter_roaster_use_case

'''
Walter Nichols
타이타닉의 일등 항해사, 승객 명단(Passenger List) 관리 담당.
'''
walter_roaster_router = APIRouter(prefix="/walter", tags=["walter"])


@walter_roaster_router.get("/myself")
async def introduce_myself(
    walter: WalterRoasterUseCase = Depends(get_walter_roaster_use_case),
) -> WalterRoasterResponse:
    return await walter.introduce_myself(WalterRoasterSchema(id=6, name="Walter Nichols"))
