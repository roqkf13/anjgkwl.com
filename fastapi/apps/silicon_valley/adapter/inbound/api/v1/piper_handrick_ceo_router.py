from fastapi import APIRouter, Depends

from silicon_valley.adapter.inbound.api.schemas.piper_handrick_ceo_schema import HandrickCeoSchema
from silicon_valley.app.dtos.piper_handrick_ceo_dto import HandrickCeoResponse
from silicon_valley.app.ports.input.piper_handrick_ceo_use_case import HandrickCeoUseCase
from silicon_valley.dependencies.piper_handrick_ceo_provider import get_handrick_ceo_use_case

'''
리처드 헨드릭스 (Richard Hendricks)
Pied Piper 창업자 겸 CEO. 중간값 압축 알고리즘을 발명했으며 사교성은 부족하지만 천재적인 엔지니어.
'''
handrick_ceo_router = APIRouter(prefix="/handrick", tags=["handrick"])


@handrick_ceo_router.get("/myself")
async def introduce_myself(
    handrick: HandrickCeoUseCase = Depends(get_handrick_ceo_use_case),
) -> HandrickCeoResponse:

    return await handrick.introduce_myself(
        HandrickCeoSchema(
            id=1,
            name="리처드 헨드릭스 (Richard Hendricks)",
        )
    )
