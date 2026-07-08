import json
import pytest

from sherlock_homes.app.use_cases.classify_spam_interactor import ClassifySpamInteractor
from sherlock_homes.app.dtos.classify_spam_dto import ClassifySpamQuery
from sherlock_homes.app.ports.output.classify_spam_llm_port import ClassifySpamLlmPort
from star_craft.domain.ontology.spam.spam_category import SpamCategory


class FakeClassifySpamLlmGateway(ClassifySpamLlmPort):

    def __init__(self, raw_response: str) -> None:
        self.raw_response = raw_response

    async def classify_raw(self, *, message: str, system: str) -> str:
        return self.raw_response


def _make_interactor(raw_response: str) -> ClassifySpamInteractor:
    return ClassifySpamInteractor(llm_gateway=FakeClassifySpamLlmGateway(raw_response))


def _llm_response(category: SpamCategory, reason: str = "테스트 이유") -> str:
    return json.dumps({"category": category.value, "reason": reason}, ensure_ascii=False)


class TestClassify:
    async def test_phishing_email(self):
        query = ClassifySpamQuery(subject="계정 확인 요청", body="비밀번호를 재설정하세요.")
        interactor = _make_interactor(_llm_response(SpamCategory.PHISHING))

        result = await interactor.classify(query)

        assert result.category == SpamCategory.PHISHING
        assert isinstance(result.reason, str)

    async def test_advertising_email(self):
        query = ClassifySpamQuery(subject="한정 특가 할인", body="지금 구매하세요!")
        interactor = _make_interactor(_llm_response(SpamCategory.ADVERTISING))

        result = await interactor.classify(query)

        assert result.category == SpamCategory.ADVERTISING

    async def test_scam_email(self):
        query = ClassifySpamQuery(subject="당신이 당첨되었습니다", body="긴급 송금이 필요합니다.")
        interactor = _make_interactor(_llm_response(SpamCategory.SCAM))

        result = await interactor.classify(query)

        assert result.category == SpamCategory.SCAM

    async def test_returns_reason(self):
        query = ClassifySpamQuery(subject="invoice", body="open attachment")
        expected_reason = "악성 첨부파일이 포함된 메일입니다."
        interactor = _make_interactor(_llm_response(SpamCategory.MALWARE, expected_reason))

        result = await interactor.classify(query)

        assert result.reason == expected_reason

    async def test_unknown_category_on_unrecognized_value(self):
        query = ClassifySpamQuery(subject="일반 메일", body="안녕하세요.")
        raw = json.dumps({"category": "unknown", "reason": "분류 불가"})
        interactor = _make_interactor(raw)

        result = await interactor.classify(query)

        assert result.category == SpamCategory.UNKNOWN

    async def test_raises_on_invalid_json(self):
        query = ClassifySpamQuery(subject="테스트", body="본문")
        interactor = _make_interactor("JSON이 아닌 응답")

        with pytest.raises(ValueError, match="JSON을 파싱하지 못했습니다"):
            await interactor.classify(query)
