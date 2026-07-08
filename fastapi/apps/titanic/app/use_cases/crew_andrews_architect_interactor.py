from __future__ import annotations

from typing import Any

from titanic.adapter.inbound.api.schemas.crew_andrews_architect_schema import AndrewsArchitectSchema
from titanic.app.dtos.crew_andrews_architect_dto import AndrewsArchitectQuery, AndrewsArchitectResponse
from titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase
from titanic.app.ports.output.crew_andrews_architect_port import AndrewsArchitectPort
from core.matrix.kiwi_oracle_morpheme_analyzer import get_kiwi, get_stopwords


class AndrewsArchitectInteractor(AndrewsArchitectUseCase):
    
    def __init__(self, repository: AndrewsArchitectPort):
        self.repository = repository

    def analyze_intent(self, messages: list) -> dict[str, Any]:
        '''Kiwi 형태소 분석으로 프론트 질문의 의도를 파악하는 메소드'''
        kiwi = get_kiwi()
        stopwords = get_stopwords()
        last_text = next((m.text for m in reversed(messages) if m.role == "user"), "")
        tokens = kiwi.tokenize(last_text, stopwords=stopwords)
        return {
            "analyzed_text": last_text,
            "tokens": [
                {"form": t.form, "tag": str(t.tag), "start": t.start, "len": t.len}
                for t in tokens
            ],
        }

    async def introduce_myself(self, schema: AndrewsArchitectSchema) -> AndrewsArchitectResponse:
        '''앤드류 설계자의 자기소개 인터렉트'''

        return await self.repository.introduce_myself(AndrewsArchitectQuery(
            id = schema.id,
            name = schema.name
        ))