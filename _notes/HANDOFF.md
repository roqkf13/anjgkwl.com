# Handoff — 2026-07-23

## 목표
1. Hermes CLI(Nous Research 에이전트)가 유료 Nous Portal 대신 로컬 Ollama를 쓰도록 Windows+WSL2에서 구성 (anjgkwl.com 코드와는 무관한 개인 도구 설정).
2. Hermes를 Claude Code의 MCP 서버로 등록해서 도구로 쓸 수 있게 함.
3. 장시간/여러 PC에 걸친 작업 연속성을 위해 이 저장소에 `_notes/`(MEMORY.md, ERRORS.md, HANDOFF.md) 기억 구조를 도입.

## 완료된 일 (검증됨)
- **Hermes + 로컬 Ollama 연결 성공.** `llama3.1:8b`로 정상 응답 확인.
  - Windows 10이라 WSL2 미러링 네트워킹 불가 → `OLLAMA_HOST=0.0.0.0` + 방화벽 허용 규칙 + (숨어있던) `ollama.exe` Public 프로필 차단 규칙 비활성화로 해결.
  - WSL→Windows 접속 IP: `172.24.240.1` (재부팅 시 바뀔 수 있음, 자세한 건 로컬 메모리 `reference_hermes_ollama_wsl_setup.md` 참고).
  - `~/.hermes/config.yaml`의 `agent.reasoning_effort: none`으로 설정 — llama3.1은 thinking 모드 미지원이라 필요했음.
- **Hermes를 MCP 서버로 등록.** 처음엔 user 스코프(`~/.claude.json`)에 등록했다가, PC 이동성 문제로 project 스코프 `.mcp.json`(저장소 루트, git 추적)으로 통일. user 스코프 쪽은 삭제함. `claude mcp list` 기준 정상 Connected.
- **`_notes/MEMORY.md`(결정 로그), `_notes/ERRORS.md`(실패 노트) 생성 및 오늘 세션 내용 소급 반영 완료.**
- **한국어 모델 컨텍스트 조사:** `exaone3.5:7.8b`(32768), `eeve-korean-10.8b`(4096), `qwen3:8b`(40960, YaRN 미적용 확인) 전부 Hermes 최소 요구치(64000) 미달로 부적합 확정.

## 진행 중인 일
- **64K 이상 지원하는 한국어 가능 모델 탐색 중단된 상태.** 다음 후보는 Gemma3(4b/12b, 공식 128K) — 아직 pull도 안 했고 실측 컨텍스트 확인도 안 됨.
- **`.mcp.json` 커밋 안 됨.** `_notes/MEMORY.md`, `_notes/ERRORS.md`도 아직 git에 안 올라간 상태 (커밋 타이밍을 물어봤으나 아직 답변 안 주심).

## 다음 행동
1. (선택) Gemma3 이어서 시도하려면: `ollama pull gemma3:4b` (Windows PowerShell) → `/api/show`로 실측 `context_length` 확인 → 통과하면 `hermes model`로 등록.
2. `_notes/MEMORY.md`, `_notes/ERRORS.md`, `.mcp.json` 커밋 여부/타이밍 확인 필요 (다른 변경사항과 묶을지, 지금 바로 할지).
3. 미뤄둔 것: `cloudflared/creds.json`이 git에 커밋돼 있는 시크릿 노출 위험 검토 ("나중에 시간 되실 때" 언급만 있었음, 착수 안 함).
4. 미뤄둔 것: 인증 게이트웨이 브라우저 실사용 테스트(Naver/Google 로그인 → JWT 발급 → `/admin` 보호 라우트 접근까지 실제로) — 하네스 구현은 끝났지만 end-to-end 브라우저 검증은 아직 안 함.

## 주의점
- **`.mcp.json`의 `wsl.exe -d Ubuntu-26.04 ...` 명령은 이 PC 전용.** 다른 PC에서 pull 받으면 WSL 배포판 이름이 다를 수 있어 연결 안 될 수 있음 — `wsl -l`로 확인 후 수정.
- **JWT 프라이빗 키 값은 절대 일부라도 화면에 보여주거나 채팅에 붙여넣지 말 것.** (이전에 실수로 노출돼서 재발급했던 전례 있음 — 공개키는 보여줘도 무방.)
- Bot Fight Mode는 완전히 꺼진 채로 유지 중, 대체 봇 방어 수단 없음.
- `friday13th_users` 테이블 리네임은 다음 RBAC 마이그레이션 때 같이 하기로 보류 중 (지금 손대지 말 것).
- 방화벽 관련 삽질(Windows 10 미러링 불가, `ollama.exe` 자동 차단 규칙)은 `_notes/ERRORS.md`와 로컬 메모리에 상세히 남아있으니, 비슷한 네트워킹 문제 생기면 거기부터 확인.
