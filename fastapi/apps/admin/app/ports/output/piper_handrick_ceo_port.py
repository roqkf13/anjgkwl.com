from __future__ import annotations

from abc import ABC, abstractmethod

from admin.app.dtos.piper_handrick_ceo_dto import HandrickCeoQuery, HandrickCeoResponse


class HandrickCeoPort(ABC):

    @abstractmethod
    def introduce_myself(self, query: HandrickCeoQuery) -> HandrickCeoResponse:
        '''리처드 헨드릭스의 자기소개 레포지토리 추상 메소드'''
        pass
