from __future__ import annotations

import re

_TOKEN_RE = re.compile(r"[가-힣A-Za-z0-9]+")
_MIN_KEYWORD_LEN = 2
_MAX_KEYWORD_LEN = 6
_MAX_CANDIDATES = 40


def extract_keyword_candidates(text: str) -> list[str]:
    """질문 문장에서 부분 문자열 검색용 키워드 후보를 뽑는다.

    "홍길동이라는" 같은 조사가 붙은 토큰에서도 "홍길동"이 후보로 나오도록,
    한글/영숫자 연속 구간의 모든 부분 문자열(길이 2~6)을 만든다.
    긴 후보일수록 더 구체적인 일치이므로 길이 내림차순으로 정렬한다.
    """
    candidates: set[str] = set()
    for run in _TOKEN_RE.findall(text):
        n = len(run)
        for length in range(min(n, _MAX_KEYWORD_LEN), _MIN_KEYWORD_LEN - 1, -1):
            for start in range(0, n - length + 1):
                candidates.add(run[start : start + length])
    # set 반복 순서는 프로세스마다 달라지므로(해시 랜덤화), 문자열 자체로도
    # 정렬해 동일 길이 후보들의 순서를 결정적으로 고정한다.
    return sorted(candidates, key=lambda c: (-len(c), c))[:_MAX_CANDIDATES]
