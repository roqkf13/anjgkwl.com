from typing import Any

from titanic.app.ports.input.walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.dtos.walter_roaster_dto import WalterRoasterQuery
from titanic.adapter.inbound.api.schemas.walter_roaster_schema import WalterRoasterSchema
from titanic.app.ports.output.walter_roaster_repository import WalterRoasterRepository
import logging

logger = logging.getLogger(__name__)


class WalterRoasterInteractor(WalterRoasterUseCase):

    def __init__(self, repository: WalterRoasterRepository) -> None:
        self._repository = repository

    def introduce_myself(self, schema: WalterRoasterSchema):
        '''월터의 자기소개 메소드'''
        query = WalterRoasterQuery(
            id=schema.id,
            name=schema.name,
            memo=schema.memo,
        )
        logger.info("########################################################")
        logger.info("🎈[월터 유스케이스] 라우터에서 가져온 월터 정보")
        logger.info(f"🎆ID: {query.id}")
        logger.info(f"🎇이름: {query.name}")
        logger.info(f"🧨메모: {query.memo}")
        logger.info("########################################################")

        self._repository.introduce_myself(query)

        pass




