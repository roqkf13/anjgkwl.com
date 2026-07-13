from fastapi import APIRouter, Depends

from admin.adapter.inbound.api.schemas.piper_dinesh_dash_schema import DineshDashSchema
from admin.app.dtos.piper_dinesh_dash_dto import DineshDashResponse
from admin.app.ports.input.piper_dinesh_dash_use_case import DineshDashUseCase
from admin.dependencies.piper_dinesh_dash_provider import get_dinesh_dash_use_case

'''
디네시 추그타이 (Dinesh Chugtai)
백엔드 엔지니어 겸 대시보드 개발 담당. 길포일과 끊임없이 경쟁하며 자신의 위상을 증명하려는 인물.
'''
dinesh_dash_router = APIRouter(prefix="/dinesh", tags=["dinesh"])


@dinesh_dash_router.get("/myself")
async def introduce_myself(
    dinesh: DineshDashUseCase = Depends(get_dinesh_dash_use_case),
) -> DineshDashResponse:

    return await dinesh.introduce_myself(
        DineshDashSchema(
            id=3,
            name="디네시 추그타이 (Dinesh Chugtai)",
        )
    )
