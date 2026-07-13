from dataclasses import dataclass

from ontology.domain.ontology.spam.spam_category import SpamCategory

'''
캐릭터: 셜록 홈즈 (Holmes)
역할 (keyword): analyst (분석가)
기능: 수신 이메일을 온톨로지 기반으로 스팸 카테고리 분류
'''


@dataclass(frozen=True)
class ClassifySpamQuery:
    subject: str
    body: str


@dataclass(frozen=True)
class ClassifySpamResult:
    category: SpamCategory
    reason: str
