"""auth — 인증 게이트웨이

스타 토폴로지의 허브/스포크 어느 쪽도 아니다. api.anjgkwl.com(비즈니스 백엔드)과
별도 컨테이너(auth.anjgkwl.com)로 배포되는 교차관심사 보안 계층으로, apps/login의
기존 유스케이스를 내부적으로 호출해 JWT(RS256)를 발급/검증/폐기한다.

의존성 방향: auth → login (허용, 이 방향만). 다른 스포크가 auth를 import하는 것은
setup.cfg의 auth-isolation 계약으로 금지된다 — 백엔드가 쓸 수 있는 건 core.dependencies뿐.
"""
