# ERRORS — 실패 노트

두세 번 이상 헤맨 접근·삽질을 기록한다. 무엇이 안 됐고, 결국 무엇이 통했는지.
같은 길에서 계속 넘어지지 않기 위한 문서.

---

## 2026-07-23

### Cloudflare Bot Fight Mode가 Vercel→백엔드 요청을 차단
**증상:** Vercel 서버리스 함수에서 백엔드(`/auth/oauth/upsert` 등)로 보내는 POST 요청이 403 "Just a moment..." 챌린지에 막힘.
**안 통한 것:**
- WAF Custom Rule로 "Skip"(건너뛰기) 설정 — Bot Fight Mode 자체를 우회 못함.
- Configuration Rules로 우회 시도 — 마찬가지로 안 통함.
**원인:** Cloudflare Analytics 이벤트 로그로 확인한 결과, AWS/Vercel 발(發) 트래픽을 "Bot Fight 모드" 서비스가 규칙 엔진보다 먼저/별도로 걸러냄 (Free 플랜 한계로 추정).
**해결:** Bot Fight Mode를 완전히 껐다.

### Docker `.env` 변경이 `docker restart`로 반영 안 됨
**증상:** `.env`/`.env.auth` 값을 고치고 `docker restart <container>`를 해도 새 값이 안 먹힘.
**원인:** `env_file:`의 값은 컨테이너 **생성 시점**에 굳어지고, `restart`는 재생성이 아니라서 안 읽힘.
**해결:** `docker compose up -d --force-recreate <service>`.
**추가 함정:** `requirements.txt`를 바꿨는데 `--force-recreate`만 하면 이미지가 안 바뀌어서 `ModuleNotFoundError`(예: `redis` 모듈 없음) 발생. `--build`까지 같이 줘야 함 → `docker compose up -d --build <service>`.

### HTTP Basic Auth에 한글 계정/비번 사용 불가
**증상:** `/docs` Basic Auth에 한글 아이디/비번을 넣으면 인증 실패.
**원인:** FastAPI/Starlette `HTTPBasic`이 `base64.b64decode(...).decode("ascii")`로 디코드 — ASCII 외 문자는 애초에 처리 불가.
**해결:** 계정/비번을 ASCII(영문+숫자)로만 구성.

### Cloudflare Tunnel 대시보드 "마이그레이션" 경고
**증상:** 로컬 관리(`cloudflared/config.yml`) 중인 터널을 대시보드에서 수정하려 하니 "마이그레이션 시작" 안내가 뜸.
**주의(실행 안 함):** 이 마이그레이션은 비가역적이고, n8n/api/ssh 등 기존 라이브 라우팅에 영향을 줄 수 있어서 클릭하지 않음.
**해결:** 로컬 `cloudflared/config.yml`을 직접 편집 + DNS CNAME은 대시보드에서 수동으로 `<tunnel-id>.cfargotunnel.com`을 가리키게 추가 (컨테이너 안 `cloudflared` CLI가 인증서 기반 인증이 없어서 `tunnel route dns` 명령 자체를 못 씀).

### Ingress 규칙 순서 실수
**증상:** 새로 추가한 `auth.anjgkwl.com` ingress 규칙이 매칭이 안 됨.
**원인:** `http_status:404` catch-all 규칙 **뒤에** 넣어서, catch-all이 먼저 걸려버림.
**해결:** catch-all보다 **앞에** 배치.

### Git 대소문자만 다른 언트랙 파일이 ff-only 머지를 막음
**증상:** `AUTH-GATEWAY-HARNESS.md`(로컬, untracked) vs `auth-gateway-harness.md`(원격에서 새로 커밋) — 대소문자만 다른 파일 충돌로 `git merge --ff-only` 실패.
**해결:** 두 파일 내용이 사실상 동일(CRLF/LF 차이만)한지 diff로 확인 → 로컬 untracked 파일을 `rm` 하고 재시도.

### WSL2 미러링 네트워킹 모드가 Windows 10에서 조용히 무시됨
**증상:** `.wslconfig`에 `networkingMode=mirrored` 설정하고 `wsl --shutdown` 해도 WSL→Windows localhost 연결이 계속 실패.
**원인:** 미러링 모드는 **Windows 11 22H2 이상 전용** 기능. Windows 10에서는 설정해도 에러 없이 그냥 무시됨.
**해결:** NAT 모드 전제로 별도 우회(`OLLAMA_HOST=0.0.0.0` + 방화벽 규칙 + WSL에서 게이트웨이 IP로 접속)로 전환. 자세한 절차는 로컬 메모리 `reference_hermes_ollama_wsl_setup.md` 참고.
**계속 참일 것들 (재발 방지용):**
- `OLLAMA_HOST` 환경변수를 설정해도 **이미 떠 있던 Ollama 앱은 반영 안 됨** — 트레이에서 완전히 종료 후 재실행해야 함.
- WSL에서 접속하는 호스트 IP(`ip route show default | awk '{print $3}'`로 확인)는 **`wsl --shutdown` 후 바뀔 수 있음** — 연결 안 되면 이 값부터 재확인.

### Windows 방화벽 — 명시적 Allow 규칙을 만들어도 계속 막힘
**증상:** `New-NetFirewallRule ... -Action Allow`로 11434 포트를 열어줬는데도 WSL에서 접속 시 타임아웃(연결 거부가 아니라 무응답).
**원인:** Ollama 설치 시 자동 생성된 것으로 보이는 `ollama.exe` 대상 **Public 프로필 차단(Block) 규칙**이 이미 존재. Windows 방화벽은 차단 규칙이 허용 규칙보다 항상 우선 적용됨.
**진단법:** `Get-NetFirewallRule -Direction Inbound -Action Block -Enabled True | Select DisplayName, Profile` 로 프로그램별 차단 규칙 확인.
**해결:** `Get-NetFirewallRule -DisplayName "ollama.exe" | Disable-NetFirewallRule`.

### `bash -lc`에 명령어를 따옴표 없이 여러 토큰으로 전달
**증상:** MCP 서버 등록 시 `bash -lc hermes mcp serve`(따옴표 없이 3토큰)로 넣었더니, `claude mcp get`에서는 "Connected"로 뜨는데 실제로는 의심스러움.
**원인:** `bash -c`는 바로 다음 토큰 **하나만** 명령 문자열로 받고, 그 뒤(`mcp`, `serve`)는 `$0`, `$1`로 빠짐 — 실제 실행되는 건 인자 없는 `hermes` 하나뿐.
**해결:** `.mcp.json`의 `args` 배열에서 `"hermes mcp serve"`를 **하나의 문자열**로 묶어서 저장. (`claude mcp add ... -- ... bash -lc 'hermes mcp serve'`처럼 셸에서 미리 따옴표로 묶어 하나의 토큰이 되게 할 것.)

### 모델 아키텍처가 지원한다 ≠ 실제 배포된 태그가 지원한다
**증상:** "Qwen3는 YaRN으로 128K까지 확장 지원한다"고 판단하고 Hermes(최소 64K 컨텍스트 요구)에 연결하려 했으나, 실제로는 부적합.
**원인:** Ollama의 `qwen3:8b` 기본 태그에는 YaRN 스케일링 설정이 적용돼 있지 않음 (`/api/show`의 `model_info`에 rope scaling 관련 필드 자체가 없음) — 실측 `context_length`는 40960.
**해결:** 모델을 새로 받을 때마다 스펙 문서를 신뢰하지 말고, `POST http://localhost:11434/api/show`로 실측 `context_length`를 직접 확인.
**참고:** `exaone3.5:7.8b`(32768), `eeve-korean-10.8b`(4096)도 같은 방식으로 확인해서 Hermes(최소 64000 요구)엔 전부 부적합 판정.

### WSL bash에서 `ollama` command not found
**증상:** `wsl.exe -d Ubuntu-26.04 -- bash -lc "ollama pull qwen3:8b"` 실행 시 `command not found`.
**원인:** Ollama는 Windows에만 설치돼 있고, WSL 안에 리눅스용 `ollama` 바이너리를 따로 설치한 적이 없음.
**해결 (두 가지):**
1. `ollama pull`/`ollama list`는 Windows PowerShell에서 실행.
2. 또는 WSL bash에서 `ollama.exe`(확장자 포함)로 호출 — WSL2가 기본적으로 Windows PATH를 WSL `$PATH`에 이어붙이는 interop 덕분에 됨. (`ollama`는 안 되고 `ollama.exe`는 됨.)
