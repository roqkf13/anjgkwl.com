from fastapi import APIRouter, Depends

from admin.adapter.inbound.api.schemas.piper_gilfoyle_system_schema import GilfoyleSystemSchema
from admin.app.dtos.piper_gilfoyle_system_dto import GilfoyleSystemResponse
from admin.app.ports.input.piper_gilfoyle_system_use_case import GilfoyleSystemUseCase
from admin.dependencies.piper_gilfoyle_system_provider import get_gilfoyle_system_use_case

'''
버트람 길포일 (Bertram Gilfoyle)
시스템 아키텍트. 인프라 및 서버 전담. 냉소적이고 무표정하지만 기술적으로는 타의 추종을 불허하는 인물.
'''
gilfoyle_system_router = APIRouter(prefix="/gilfoyle", tags=["gilfoyle"])


@gilfoyle_system_router.get("/myself")
async def introduce_myself(
    gilfoyle: GilfoyleSystemUseCase = Depends(get_gilfoyle_system_use_case),
) -> GilfoyleSystemResponse:

    return await gilfoyle.introduce_myself(
        GilfoyleSystemSchema(
            id=4,
            name="버트람 길포일 (Bertram Gilfoyle)",
        )
    )
