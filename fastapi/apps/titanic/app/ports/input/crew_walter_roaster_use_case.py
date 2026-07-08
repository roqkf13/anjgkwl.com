from abc import ABC, abstractmethod

import pandas as pd
from titanic.adapter.inbound.api.schemas.crew_walter_roaster_schema import WalterRoasterSchema
from titanic.app.dtos.crew_walter_roaster_dto import WalterRoasterResponse

class WalterRoasterUseCase(ABC):

    @abstractmethod
    async def introduce_myself(self, schema: WalterRoasterSchema) -> WalterRoasterResponse:
        '''월터의 자기소개 메소드'''
        pass

    @abstractmethod
    async def load(self) -> None:
        '''DB에서 train/test set을 가져와 캐싱하는 메소드'''
        pass

    @abstractmethod
    def get_train_set(self) -> pd.DataFrame:
        '''캐싱된 train set을 반환하는 메소드'''
        pass

    @abstractmethod
    def get_test_set(self) -> pd.DataFrame:
        '''캐싱된 test set을 반환하는 메소드'''
        pass