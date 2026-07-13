from enum import Enum


class SpamCategory(str, Enum):
    PHISHING = "phishing"           # 피싱 — 계정·결제 정보 탈취
    ADVERTISING = "advertising"     # 광고 — 무단 상업 메일
    SCAM = "scam"                   # 사기 — 금전 편취 목적
    MALWARE = "malware"             # 악성코드 — 첨부파일·링크 포함
    SOCIAL_ENGINEERING = "social_engineering"  # 사회공학 — 신뢰 관계 위장
    UNKNOWN = "unknown"             # 분류 불가
