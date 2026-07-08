from dataclasses import dataclass, field

from apps.star_craft.domain.ontology.spam.spam_category import SpamCategory


@dataclass(frozen=True)
class SpamNode:
    category: SpamCategory
    description: str
    keywords: tuple[str, ...]
    children: tuple["SpamNode", ...] = field(default_factory=tuple)


SPAM_TAXONOMY: tuple[SpamNode, ...] = (
    SpamNode(
        category=SpamCategory.PHISHING,
        description="계정·결제 정보 탈취를 목적으로 공식 기관을 사칭하는 메일",
        keywords=("계정 확인", "비밀번호 재설정", "로그인 시도", "결제 정보 업데이트", "verify your account"),
    ),
    SpamNode(
        category=SpamCategory.ADVERTISING,
        description="수신 동의 없이 발송된 상업성 광고 메일",
        keywords=("할인", "무료", "한정 특가", "지금 구매", "unsubscribe", "수신거부"),
    ),
    SpamNode(
        category=SpamCategory.SCAM,
        description="금전 편취를 목적으로 허위 사실을 주장하는 메일",
        keywords=("당첨", "송금", "유산", "투자 수익", "긴급 송금", "you have won"),
    ),
    SpamNode(
        category=SpamCategory.MALWARE,
        description="악성 첨부파일 또는 링크를 통해 시스템을 감염시키려는 메일",
        keywords=("첨부파일 확인", "invoice", "배송 조회", "open attachment", "click here"),
    ),
    SpamNode(
        category=SpamCategory.SOCIAL_ENGINEERING,
        description="신뢰 관계를 위장하여 민감한 행동을 유도하는 메일",
        keywords=("CEO", "긴급 요청", "비밀 유지", "즉시 처리", "urgent request"),
    ),
    SpamNode(
        category=SpamCategory.UNKNOWN,
        description="위 카테고리로 분류되지 않는 스팸",
        keywords=(),
    ),
)

TAXONOMY_INDEX: dict[SpamCategory, SpamNode] = {node.category: node for node in SPAM_TAXONOMY}
