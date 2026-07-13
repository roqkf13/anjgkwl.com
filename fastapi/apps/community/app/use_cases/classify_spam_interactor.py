from __future__ import annotations

import json
import re

from community.app.dtos.classify_spam_dto import ClassifySpamQuery, ClassifySpamResult
from community.app.ports.input.classify_spam_use_case import ClassifySpamUseCase
from community.app.ports.output.classify_spam_llm_port import ClassifySpamLlmPort
from ontology.domain.ontology.spam.spam_category import SpamCategory
from ontology.domain.ontology.spam.spam_taxonomy import TAXONOMY_INDEX

_SYSTEM_PROMPT = """\
당신은 이메일 스팸 분류 전문가입니다.
주어진 이메일의 제목과 본문을 분석하여 아래 카테고리 중 하나로 분류하세요.

카테고리:
{taxonomy}

반드시 아래 JSON 형식으로만 응답하세요. 추가 설명 없이 JSON만 출력하세요.
{{"category": "<카테고리 값>", "reason": "<한 문장 이유>"}}\
"""


def _build_system_prompt() -> str:
    lines = [
        f"- {node.category.value}: {node.description}"
        for node in TAXONOMY_INDEX.values()
        if node.category is not SpamCategory.UNKNOWN
    ]
    return _SYSTEM_PROMPT.format(taxonomy="\n".join(lines))


class ClassifySpamInteractor(ClassifySpamUseCase):

    def __init__(self, llm_gateway: ClassifySpamLlmPort) -> None:
        self._llm_gateway = llm_gateway

    async def classify(self, query: ClassifySpamQuery) -> ClassifySpamResult:
        message = f"제목: {query.subject}\n본문: {query.body}"
        raw = await self._llm_gateway.classify_raw(message=message, system=_build_system_prompt())
        return self._parse(raw)

    def _parse(self, raw: str) -> ClassifySpamResult:
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            data = json.loads(match.group())
            category = SpamCategory(data.get("category", SpamCategory.UNKNOWN))
            return ClassifySpamResult(category=category, reason=data.get("reason", ""))
        raise ValueError(f"EXAONE 응답에서 JSON을 파싱하지 못했습니다: {raw[:200]}")
