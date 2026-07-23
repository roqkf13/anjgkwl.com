# MEMORY — 결정 로그

방향·형식·전략·중요한 선택이 생기면 무엇을 결정했고 왜 그렇게 했는지 기록한다.
다음 세션의 Claude가 같은 결정을 다시 흔들지 않게 하기 위함.
CLAUDE.md는 "지금 어떻게 해야 하는지"(현재형 규칙), 이 문서는 "왜 그렇게 하기로 했는지"(과거형 히스토리)를 담는다.

---

## 2026-07-23

### Naver 로그인 UX — 팝업 방식 채택
전체 페이지 이동(direct navigation) 대신 팝업 창을 띄우고 `localStorage` + `storage` 이벤트로 결과를 메인 창에 전달하는 방식으로 구현.
**왜:** 메인 페이지가 이동해버리지 않게 하기 위함(사용자 요청). Google OAuth는 COOP(Cross-Origin-Opener-Policy) 헤더 때문에 `window.opener` 직접 참조가 막혀서, `postMessage`가 아니라 `localStorage`+`storage` 이벤트 조합을 씀.
관련 파일: `nextjs/v0-titanic-qa-app/app/login/page.tsx`, `app/oauth-complete/page.tsx`, `lib/oauth-result.ts`.

### Google OAuth 전용 프로젝트로 분리
기존에 n8n과 공유하던 "n8n-gmail" Google Cloud 프로젝트에서, Scout/로그인 전용 "scout" 프로젝트로 마이그레이션.
**왜:** 프로젝트명이 실제 용도와 안 맞고(오해 소지), 서로 다른 서비스가 credential을 공유하는 게 바람직하지 않음.
**주의:** 전환 시 새 클라이언트로 전환 → 검증 → 재시작까지 끝난 뒤에 옛 클라이언트를 삭제하는 순서를 지킬 것 (즉시 삭제하면 라이브 로그인이 끊길 위험).

### FastAPI `/docs` `/redoc` `/openapi.json` Basic Auth로 보호
RBAC 전체 구현 전에 우선 가볍게 막아둠.
**왜:** 문서 엔드포인트가 공개돼 있던 걸 빠르게 틀어막을 필요가 있었고, 전체 RBAC는 별도 작업이라 시간이 더 걸림.
**주의:** Starlette `HTTPBasic`은 ASCII만 디코드하므로 계정/비번은 영문+숫자로.

### Cloudflare Bot Fight Mode 전면 비활성화
WAF Custom Rule "Skip"이나 Configuration Rule로는 Bot Fight Mode를 우회할 수 없음이 Cloudflare Analytics 이벤트 로그로 확인됨 (Free 플랜 한계).
**왜:** Vercel(서버리스)→백엔드 POST 요청이 "Just a moment..." 챌린지에 막혀서 Naver/Google 콜백 처리가 실패했음.
**결정:** Bot Fight Mode 자체를 껐다. 다른 봇 방어 수단으로 대체하지 않음 — 필요해지면 나중에 재검토.

### 인증 게이트웨이(`auth.anjgkwl.com`) 신규 구축
`fastapi/apps/auth/_docs/auth-gateway-harness.md` 하네스 스펙대로 RS256 JWT 발급/검증, RBAC(RoleChecker), Google+Naver OAuth를 `apps/auth`에 독립 재구현, Redis 기반 리프레시 토큰 세션+재사용 탐지, 별도 `auth_main.py` 엔트리포인트로 구축.
**왜:** 기존 friday13th_users/login 앱과 결합도를 낮추고, 인증을 독립 서비스로 분리해 여러 앱이 공유하는 구조로 가기 위함.
**설계 편차(하네스 대비):**
- `auth_router`를 `/auth` 프리픽스 없이 등록 — `auth.anjgkwl.com/auth/...`처럼 경로가 중복되는 걸 피하기 위함.
- `GET /login/{provider}` 엔드포인트 추가 — 하네스엔 `/callback`만 명시돼 있었지만, OAuth 흐름을 시작시킬 진입점이 필요해서 추가.
- `import-linter`의 `auth-isolation` 계약으로 다른 모든 스포크 앱이 `apps.auth`를 직접 import하지 못하게 강제 — `core/dependencies.py`(`get_current_user`, `RoleChecker`)만 공용 진입점.
- docker-compose `auth` 서비스는 `ports:` 매핑 없음 — Cloudflare Tunnel을 통해서만 진입 허용 (하네스의 절대 규칙).

### Naver "동의 화면 게이팅" 기능 구현 후 되돌림
`signPendingProfile`, `/signup/naver-consent`, `/api/auth/naver/complete`, `/auth/oauth/lookup`, `find_oauth_user` 유스케이스까지 전부 구현했다가 전체 되돌림(revert).
**왜:** Naver 자체 동의 화면으로 충분하다고 최종 판단 — 별도 자체 동의 게이팅 UI가 불필요한 중복이었음.

### `friday13th_users` 테이블 리네임 보류
지금 당장 안 하고, 다음 RBAC 관련 마이그레이션 때 묶어서 처리하기로 함.
**왜:** 마이그레이션을 여러 번 나눠서 하기보다 관련 있는 스키마 변경을 한 번에 묶는 게 효율적.

### 소통 방식·지침 저장 원칙을 CLAUDE.md에 반영
"채팅 응답은 한글로", "지속적 지침은 로컬 메모리 아니라 CLAUDE.md에 커밋" 두 조항을 루트 `CLAUDE.md`에 추가.
**왜:** 로컬 메모리에만 남기면 다른 PC로 옮겼을 때 사라짐 — git으로 동기화되는 문서에 남겨야 어느 PC에서든 동일하게 적용됨.

### 이 저장소 관련 없는 개인 도구 설정은 CLAUDE.md 대신 로컬 메모리로
(Hermes CLI + Ollama WSL 설정 등) — anjgkwl.com 코드와 무관한 개인 작업 습관/도구 설정은 프로젝트 CLAUDE.md를 지저분하게 만들지 않기 위해 로컬 메모리(Claude 자동 메모리 시스템)에 남기기로 함. 단, 여러 PC를 오가며 반복해야 하는 절차라 로컬 메모리만으로는 부족하다고 판단, `_notes/`(이 폴더)에도 별도 참고문서를 두기로 함(git으로 동기화되어 PC 간 이동 가능).
