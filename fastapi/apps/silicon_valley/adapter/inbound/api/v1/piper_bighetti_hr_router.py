from fastapi import APIRouter, Depends

from silicon_valley.adapter.inbound.api.schemas.piper_bighetti_hr_schema import BighettiHrSchema
from silicon_valley.app.dtos.piper_bighetti_hr_dto import BighettiHrResponse
from silicon_valley.app.ports.input.piper_bighetti_hr_use_case import BighettiHrUseCase
from silicon_valley.dependencies.piper_bighetti_hr_provider import get_bighetti_hr_use_case

'''
넬슨 빅헤드 비게티 (Nelson "Big Head" Bighetti)
Pied Piper 공동창업자. 아무것도 안 해도 운으로 거대한 성공을 이룬 HR 담당.
'''
bighetti_hr_router = APIRouter(prefix="/bighetti", tags=["bighetti"])


@bighetti_hr_router.get("/myself")
async def introduce_myself(
    bighetti: BighettiHrUseCase = Depends(get_bighetti_hr_use_case),
) -> BighettiHrResponse:

    return await bighetti.introduce_myself(
        BighettiHrSchema(
            id=5,
            name="넬슨 빅헤드 비게티 (Nelson Bighetti)",
        )
    )
