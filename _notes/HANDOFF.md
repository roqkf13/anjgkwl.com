# Handoff — 2026-07-23

## 목표
1. Hermes CLI(Nous Research 에이전트)가 유료 Nous Portal 대신 로컬 Ollama를 쓰도록 Windows+WSL2에서 구성 (anjgkwl.com 코드와는 무관한 개인 도구 설정).
2. Hermes를 Claude Code의 MCP 서버로 등록해서 도구로 쓸 수 있게 함.
3. 장시간/여러 PC에 걸친 작업 연속성을 위해 이 저장소에 `_notes/`(MEMORY.md, ERRORS.md, HANDOFF.md) 기억 구조를 도입.

## 완료된 일 (검증됨)
- **Hermes + 로컬 Ollama 연결 성공.** `llama3.1:8b`로 정상 응답 확인.
  - Windows 10이라 WSL2 미러링 네트워킹 불가 → `OLLAMA_HOST=0.0.0.0` + 방화벽 허용 규칙 + (숨어있던) `ollama.exe` Public 프로필 차단 규칙 비활성화로 해결.
  - WSL→Windows 접속 IP: `172.24.240.1` (재부팅 시 바뀔 수 있음 — 이 사실 `_notes/ERRORS.md`에도 기록해둠).
  - `~/.hermes/config.yaml`의 `agent.reasoning_effort: none`으로 설정 — llama3.1은 thinking 모드 미지원이라 필요했음.
- **Hermes를 MCP 서버로 등록, `.mcp.json`(project 스코프) 하나로 정리 완료.** user 스코프 등록은 삭제. `claude mcp list` 기준 정상 Connected (첫 `claude` 실행 시 프로젝트 MCP 신뢰 승인 필요 — 정상 동작).
- **`_notes/MEMORY.md`(결정 로그) / `ERRORS.md`(실패 노트) / `HANDOFF.md`(이 파일) 구조 도입, 오늘 세션 내용 반영 완료.** 루트 `CLAUDE.md`에도 이 구조를 참조하라는 포인터 추가함.
- **한국어 모델 컨텍스트 조사:** `exaone3.5:7.8b`(32768), `eeve-korean-10.8b`(4096), `qwen3:8b`(40960, YaRN 미적용 확인) 전부 Hermes 최소 요구치(64000) 미달로 부적합 확정.
- **협업 습관 교정 반영:** "반복 질문에 근거 없이 뒤집지 않기"를 루트 `CLAUDE.md`에 추가 (교차 검증성 재질문과 진짜 새 근거로 인한 정정을 구분하기).
- **모든 변경사항 커밋 + push 완료.** `henry` 브랜치, origin과 동기화됨 (마지막 커밋 `1bf39db`).

## 진행 중인 일
- **64K 이상 지원하는 한국어 가능 모델 탐색이 중단된 상태.** 다음 후보는 Gemma3(4b/12b, 공식 128K) — 아직 pull도 안 했고 실측 컨텍스트 확인도 안 됨.

## 다음 행동
1. (선택) Gemma3 이어서 시도하려면: `ollama pull gemma3:4b` (Windows PowerShell) → `/api/show`로 실측 `context_length` 확인 → 통과하면 `hermes model`로 등록.
2. henry 브랜치가 main/abi와 갈라진 상태인지 확인하고, 필요하면 CLAUDE.md 브랜치 전략대로 main에 PR 올리기 (오늘 세션에서 시작 안 함).
3. 미뤄둔 것: `cloudflared/creds.json`이 git에 커밋돼 있는 시크릿 노출 위험 검토 ("나중에 시간 되실 때" 언급만 있었음, 착수 안 함).
4. 미뤄둔 것: 인증 게이트웨이 브라우저 실사용 테스트(Naver/Google 로그인 → JWT 발급 → `/admin` 보호 라우트 접근까지 실제로) — 하네스 구현은 끝났지만 end-to-end 브라우저 검증은 아직 안 함.

## 주의점
- **`.mcp.json`의 `wsl.exe -d Ubuntu-26.04 ...` 명령은 이 PC 전용.** 다른 PC에서 pull 받으면 WSL 배포판 이름이 다를 수 있어 연결 안 될 수 있음 — `wsl -l`로 확인 후 수정.
- **JWT 프라이빗 키 값은 절대 일부라도 화면에 보여주거나 채팅에 붙여넣지 말 것.** (이전에 실수로 노출돼서 재발급했던 전례 있음 — 공개키는 보여줘도 무방.)
- Bot Fight Mode는 완전히 꺼진 채로 유지 중, 대체 봇 방어 수단 없음.
- `friday13th_users` 테이블 리네임은 다음 RBAC 마이그레이션 때 같이 하기로 보류 중 (지금 손대지 말 것).
- 방화벽 관련 삽질(Windows 10 미러링 불가, `ollama.exe` 자동 차단 규칙)은 `_notes/ERRORS.md`와 로컬 메모리에 상세히 남아있으니, 비슷한 네트워킹 문제 생기면 거기부터 확인.
