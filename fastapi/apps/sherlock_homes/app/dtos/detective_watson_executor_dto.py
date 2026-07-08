from dataclasses import dataclass

'''
캐릭터: 존 왓슨 (John H. Watson)
역할 (keyword): executor (실행/조율자)
드라마 설정 및 시스템 기능: 셜록의 파트너인 사설 탐정 조력자.
탐정의 추론 결과를 실제 현실 세계의 액션과 인간의 언어(블로그 등)로 번역하고 최종 사용자 인터페이스를 조율 및 실행합니다.
'''


@dataclass(frozen=True)
class WatsonExecutorQuery:
    id: int
    name: str


@dataclass(frozen=True)
class WatsonExecutorResponse:
    id: int
    name: str


@dataclass(frozen=True)
class WatsonSendEmailQuery:
    to: str
    prompt: str
    from_account: str


@dataclass(frozen=True)
class WatsonSendEmailResult:
    message: str
    subject: str
    to: str
