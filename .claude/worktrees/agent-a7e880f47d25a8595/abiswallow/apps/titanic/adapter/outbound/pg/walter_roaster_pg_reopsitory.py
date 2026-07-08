import logging

from sqlalchemy.ext.asyncio import AsyncSession

from titanic.app.dtos.walter_roaster_dto import WalterRoasterQuery
from titanic.app.ports.output.walter_roaster_repository import WalterRoasterRepository

logger = logging.getLogger(__name__)


class WalterRoasterPgRepository(WalterRoasterRepository):
    '''PostgreSQL을 이용한 월터의 승객 명단 관리 저장소'''

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def introduce_myself(self, query: WalterRoasterQuery):
        '''승객 명단을 가져오는 메소드'''
        # PostgreSQL에서 승객 명단을 가져오는 로직 구현
        logger.info("###############################################")
        logger.info("🎈[월터 레포지토리] 유스케이스에서 가져온 월터 정보")
        logger.info(f"🎆ID: {query.id}")
        logger.info(f"🎇이름: {query.name}")
        logger.info(f"🧨메모: {query.memo}")
        logger.info("###############################################")
        pass
