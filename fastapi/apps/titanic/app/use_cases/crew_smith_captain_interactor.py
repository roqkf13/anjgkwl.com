from __future__ import annotations

import asyncio
import logging
import re

from pandas import DataFrame

from titanic.adapter.inbound.api.schemas.crew_smith_captain_schema import (
    ChatResponse,
    ChatSchema,
    SmithCaptainSchema,
)
from titanic.app.dtos.crew_smith_captain_dto import SmithCaptainQuery, SmithCaptainResponse
from titanic.app.ports.input.crew_andrews_architect_use_case import AndrewsArchitectUseCase
from titanic.app.ports.input.crew_hartley_violin_use_case import HartleyViolinUseCase
from titanic.app.ports.input.crew_lowe_boat_use_case import LoweBoatUseCase
from titanic.app.ports.input.crew_smith_captain_use_case import SmithCaptainUseCase
from titanic.app.ports.input.crew_walter_roaster_use_case import WalterRoasterUseCase
from titanic.app.ports.input.passenger_jack_trainer_use_case import JackTrainerUseCase
from titanic.app.ports.input.passenger_rose_model_use_case import RoseModelUseCase
from titanic.app.ports.input.passenger_cal_tester_use_case import CalTesterUseCase
from titanic.app.ports.output.crew_smith_captain_port import SmithCaptainPort

logger = logging.getLogger(__name__)


_CORRELATION_CONTEXT = """\
=== 생존 상관관계 순위 (5개 Value Object 기준) ===
1. gender (성별)             r = +0.543  여성일수록 생존 확률 높음 (여성·아이 우선 대피 원칙)
2. title (호칭)              r = +0.371  Mr·Miss·Mrs·Master·Royal·Rare; 성별·사회적 지위 내포
3. pclass (객실등급)         r = −0.338  1등석=1, 3등석=3; 등급 낮을수록 생존율 하락
4. cabin_assigned (객실배정) r = +0.317  객실 번호 보유 여부; 1등석 탑승 지표로 작용
5. fare (운임)               r = +0.257  티켓 요금 높을수록 생존 확률 높음
6. embarked (탑승항)         r = −0.170  Southampton 출발 3등석 승객 비율 높아 음의 관계"""


class SmithCaptainInteractor(SmithCaptainUseCase):

    def __init__(self, repository, andrews, jack, rose, cal, walter, lowe, hartley):
        self.repository: SmithCaptainPort = repository
        self.andrews: AndrewsArchitectUseCase = andrews
        self.jack: JackTrainerUseCase = jack
        self.rose: RoseModelUseCase = rose
        self.cal: CalTesterUseCase = cal
        self.walter: WalterRoasterUseCase = walter
        self.lowe: LoweBoatUseCase = lowe
        self.hartley: HartleyViolinUseCase = hartley

    async def chat(self, schema: ChatSchema) -> ChatResponse:
        await self.walter.load()
        train_set = self.walter.get_train_set()
        answer = await asyncio.to_thread(self._process_chat, schema, train_set)
        return ChatResponse(text=answer)

    def _process_chat(self, schema: ChatSchema, train_set: DataFrame) -> str:
        from core.matrix.ollama_neo_local_model import generate_reply_ollama as generate_reply
        from titanic.adapter.outbound.orm.passenger_rose_model_strategies import (
            RandomForestStrategy,
            _build_training_set,
        )

        question = next(
            (m.text for m in reversed(schema.messages) if m.role == "user"), ""
        )

        records = train_set.to_dict("records")
        X, y, age_med, fare_med = _build_training_set(records)

        rf = RandomForestStrategy()
        if X:
            rf.fit(X, y)

        total = len(records)
        survived_cnt = sum(1 for r in records if str(r.get("survived", "")) == "1")
        prediction_section = _build_prediction_section(question, X, rf, age_med, fare_med)

        prompt = f"""당신은 타이타닉 생존 분석 AI 어시스턴트입니다.
아래 분석 데이터를 참고하여 한국어로 답변하세요. 3~5문장 이내로 간결하게 작성하세요.

=== 타이타닉 학습 데이터 요약 ===
승객 수: {total}명 | 생존: {survived_cnt}명 ({survived_cnt / total * 100:.1f}%) | 사망: {total - survived_cnt}명

{_CORRELATION_CONTEXT}
{prediction_section}
=== 사용자 질문 ===
{question}"""

        return generate_reply(message=prompt)

    async def introduce_myself(self, schema: SmithCaptainSchema) -> SmithCaptainResponse:
        return await self.repository.introduce_myself(SmithCaptainQuery(
            id=schema.id,
            name=schema.name,
        ))


def _build_prediction_section(
    question: str,
    X: list,
    rf: object,
    age_med: float,
    fare_med: float,
) -> str:
    """나이·성별 키워드가 감지되면 RandomForest 생존 확률을 계산해 반환한다."""
    from titanic.adapter.outbound.orm.passenger_rose_model_strategies import _to_feature_vector

    if not X:
        return ""

    age_m = re.search(r"(\d+)\s*(?:세|살)", question)
    gender_m = re.search(r"(남자|남성|여자|여성)", question)
    if not (age_m and gender_m):
        return ""

    age = float(age_m.group(1))
    gender_raw = gender_m.group(1)
    pclass_m = re.search(r"([123])\s*등석", question)
    pclass = int(pclass_m.group(1)) if pclass_m else 2

    fv = _to_feature_vector(
        {
            "gender": "male" if gender_raw in ("남자", "남성") else "female",
            "age": age,
            "pclass": pclass,
            "fare": fare_med,
            "embarked": "S",
            "sibsp": 0,
            "parch": 0,
        },
        age_med,
        fare_med,
    )
    prob = rf.predict_proba([fv])[0]
    verdict = "생존 가능성 높음" if prob >= 0.5 else "사망 가능성 높음"

    return (
        f"\n=== 예측 결과 ===\n"
        f"입력 조건: {gender_raw} {age:.0f}세 {pclass}등석\n"
        f"Random Forest 생존 확률: {prob:.1%} → {verdict}\n\n"
    )
