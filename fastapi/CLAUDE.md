# fastapi — 백엔드 프로젝트

Python FastAPI 기반 **모듈러 모놀리식** 서버. 일반 지침은 루트 `CLAUDE.md` 참조.

## 아키텍처 개요: 스타 토폴로지 (Star Topology)

헥사고날 클린 아키텍처(선형 구조)를 기반으로 유지하면서, 앱 간 통신에는 비선형 스타 토폴로지를 추가로 적용한다. 두 구조는 중첩된다.

`apps/` 안의 모듈들은 **스타 토폴로지** 구조를 따른다.

```
        login
            │
scout ── ontology ── titanic
          (...)
```

### Hub / Spoke 역할

| 역할 | 앱 | 책임 |
|------|----|------|
| Hub | `ontology` | 전역 온톨로지 인덱스, 컨텍스트 라우팅, 앱 간 오케스트레이션 |
| Spoke | 그 외 모든 앱 | 독립 도메인 로직; 타 앱과의 통신은 반드시 hub를 경유 |

### 의존성 방향 규칙

| 방향 | 허용 여부 |
|------|----------|
| 스포크 → 허브 | ✅ 허용 |
| 허브 → 스포크 | ✅ 허용 (오케스트레이션 목적) |
| 스포크 → 스포크 (직접) | ❌ **금지** |
| 스포크 간 순환 참조 | ❌ **금지** |

스포크 간 직접 import가 필요해 보이는 경우, hub(`ontology`)에 오케스트레이션 로직을 추가하는 것이 올바른 방법이다.  
이 규칙은 코드 리뷰와 `import-linter`로 강제한다.

### 하네스 검증 (Harness Engineering)

구조적 제약이 깨지지 않도록 다음 도구들이 배선(harness)처럼 항상 작동한다.

| 레이어 | 도구 | 파일 |
|--------|------|------|
| Python 의존성 규칙 | `import-linter` | `setup.cfg` |
| MD 온톨로지 구조 검증 | 커스텀 스크립트 | `scripts/validate-harness.py` |
| MD 린팅 | `markdownlint` | `.markdownlint.json` |
| MD 포매팅 | `prettier` | `.prettierrc` |

- **정적 분석**: `setup.cfg`의 import-linter 규칙이 스포크 간 직접 import를 CI에서 차단.
- **온톨로지 검증**: MD 파일은 허브/스포크 노드로 취급하며, frontmatter에 `type`과 `links` 필드를 포함해야 함. `validate-harness.py`가 위반 여부를 검사.
- **테스트**: 허브의 라우팅 로직은 단위 테스트로 커버. 스포크는 허브 없이 독립 테스트 가능해야 함.
- **아키텍처 문서**: 새 앱 추가 시 허브/스포크 역할을 `apps/<name>/__init__.py` 상단 docstring에 명시.

### MD 온톨로지 노드 스키마

지식 베이스의 MD 파일은 허브 또는 스포크 노드로 선언한다.

```yaml
# 허브 노드 예시
---
type: hub
id: ontology
title: "Ontology Hub"
links:
  - login
  - scout
  - titanic
---

# 스포크 노드 예시
---
type: spoke
id: login
title: "Login — 회원/인증"
links:
  - ontology
---
```

규칙: `links`에 다른 스포크 ID를 직접 넣으면 `validate-harness.py`가 위반으로 감지한다.

---

## 기술 스택

- **FastAPI 0.137** + **Uvicorn**
- **SQLAlchemy 2 (asyncio)** + **asyncpg** (Neon PostgreSQL)
- **Alembic** (DB 마이그레이션) + **SQLModel**
- **Google GenAI** (Gemini) + **Ollama** (로컬 LLM)
- **pytest** (`asyncio_mode = auto`)

## 디렉토리 구조

```
fastapi/
├── main.py              ← FastAPI 앱 진입점, 라우터 등록
├── core/                ← 공유 설정, DB 엔진 (matrix/)
├── adapters/            ← 공유 어댑터 (DB 헬스 등)
├── alembic/             ← DB 마이그레이션
└── apps/                ← 도메인별 앱 모듈
    ├── ontology/        ← [허브] 전역 온톨로지 인덱스, 컨텍스트 라우팅, 앱 간 오케스트레이션
    ├── login/           ← [스포크] 회원/인증
    ├── scout/           ← [스포크] 게임 추천
    ├── titanic/         ← [스포크] Titanic 예측
    └── ...
```

각 앱은 **헥사고날 아키텍처**를 따른다.

```
apps/<name>/
├── adapter/
│   ├── inbound/api/     ← FastAPI 라우터
│   └── outbound/orm/    ← SQLAlchemy 모델·리포지토리
├── app/                 ← 유스케이스
└── domain/
    ├── entities/
    └── value_objects/
```

## 개발 / 실행

```bash
# fastapi/ 루트에서
uvicorn main:app --reload
```

## 테스트

```bash
pytest                   # 전체 (빠른 테스트)
pytest -m "not ollama"   # Ollama 없는 환경에서
pytest -m ollama         # Ollama 로컬 서버 필요
```

## 마이그레이션

```bash
alembic revision --autogenerate -m "설명"
alembic upgrade head
```

## 배포 환경 — 로컬 vs 원격 서버 `.env` 주의

`.env`는 `.gitignore`에 포함되어 **git으로 동기화되지 않는다**. 로컬 Windows 머신의 `fastapi/.env`와 원격 서버(`ssh.anjgkwl.com`)의 `fastapi/.env`는 **완전히 별개의 파일**이다.

- 로컬 `.env`에 값을 추가/수정해도 원격 서버에는 **자동 반영되지 않는다**. 브랜치 머지·PR과도 무관하다(애초에 git에 안 올라감).
- 원격 서버 쪽 설정(예: `OLLAMA_MODEL` 값, Ollama에 어떤 모델이 설치돼 있는지)은 **가정하지 말고 그 세션에서 직접 SSH로 확인**한다. 로컬 세션의 기억과 원격 서버의 실제 상태는 다를 수 있다.
- 원격 서버는 `docker-compose.yaml`의 `backend` 서비스가 `env_file: ./fastapi/.env`로 값을 읽는다. `.env`를 바꿔도 **컨테이너를 재시작(재빌드)하기 전까지는 반영되지 않는다** — 재기동 후 실제로 반영됐는지 확인한다.

## 로컬 개발 — 도커 컨테이너가 이미 8000번 포트를 쓰고 있을 수 있음

로컬(Windows/WSL)에서도 `docker-compose.yaml`로 전체 스택(backend, pgvector, redis, n8n, neo4j 등)이 이미 떠 있는 경우가 많다. `uvicorn main:app --reload`로 로컬에서 직접 띄우기 전에 반드시 확인한다.

- 먼저 `docker ps`로 `anjgkwlcom-backend-1` 컨테이너가 이미 8000번 포트를 물고 있는지 확인한다. 물고 있으면 로컬에서 uvicorn을 새로 띄울 때 `[Errno 98] Address already in use` 에러가 나는 게 정상이고, 그 컨테이너가 실제로 요청을 처리하고 있는 백엔드다. `curl`로 테스트했다면 그 응답도 로컬 프로세스가 아니라 이 컨테이너가 준 것이다.
- `backend` 서비스는 `./fastapi:/app`로 소스를 볼륨 마운트하지만, 컨테이너 `Dockerfile`의 `CMD`에 `--reload` 옵션이 없다. 즉 코드를 수정하면 파일은 컨테이너 안에 즉시 반영되지만(볼륨 마운트라서), 이미 떠 있는 uvicorn 프로세스는 **재시작 전까지 그 변경을 반영하지 않는다**.
- 코드를 바꾼 뒤 동작을 확인하려면: `docker restart anjgkwlcom-backend-1` (`requirements.txt`를 안 건드렸다면 재빌드는 불필요) 후 `docker logs -f anjgkwlcom-backend-1`로 에러 없이 떴는지 확인하고 나서 테스트한다.
- **LLM(Claude)이 이 세션에서 직접 셸에 접근할 수 있는 경우, 사용자에게 재시작을 요청하지 말고 `docker restart anjgkwlcom-backend-1`을 직접 실행한다.** 코드나 `.env`를 수정한 뒤 동작 확인이 필요하면 재시작 → `docker logs`로 에러 확인 → 테스트까지 이어서 진행한다.

## 컨벤션

- 새 앱은 `apps/` 아래 헥사고날 구조로 추가하고 `main.py`에 라우터 등록.
- 새 앱 추가 시 허브/스포크 여부를 `apps/<name>/__init__.py` 상단 docstring에 명시.
- 스포크에서 다른 스포크를 직접 import하지 않는다. 허브(`ontology`)를 경유한다.
- DB 모델은 `adapter/outbound/orm/`, 도메인 엔티티는 `domain/entities/`에 분리.
- 엔드포인트는 `async def` 기본. 동기 처리가 꼭 필요한 경우에만 `def`.
- 느린 LLM 테스트는 `@pytest.mark.ollama`로 마킹.

## 상세 개발 컨벤션

엔티티/DB 규칙, 네이밍 규칙, ML 데이터 분석 원칙, async/sync 선택 기준 등 세부 컨벤션은 `_docs/CLAUDE.md`에 있다. 관련 작업을 할 때 참고한다.
