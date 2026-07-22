# Backend (fastapi) 지침

## 프로젝트 개요

Karpathy의 Harness Engineering 프로세스를 적용한 PKS(Personal Knowledge System).  
Wiki + LLM을 결합하며, `apps/` 하위에 독립 앱들이 시블링으로 확장된다.

- **런타임**: Python 3.13, FastAPI, SQLAlchemy async, Uvicorn
- **DB**: PostgreSQL (Neon serverless), SQLModel/SQLAlchemy ORM
- **LLM**: Google Gemini (`google-genai`), Ollama (로컬)
- **형태소**: kiwipiepy (한국어)
- **인프라**: Docker Compose (`./fastapi:/app` 볼륨 마운트)
- **엔트리포인트**: `main.py` (포트 8000)

---

## 아키텍처 원칙

모든 코드는 예외 없이 아래를 준수한다.

- **SOLID** — Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **Hexagonal Architecture** (Ports & Adapters) — 도메인 로직은 인프라에 의존하지 않는다
- **Clean Architecture** — 의존성 화살표는 항상 안쪽을 향한다 (`domain ← application ← adapter`)
- **DDD** — 엔티티, 값 객체, 애그리거트, 레포지토리, 유스케이스를 명시적으로 모델링한다

---

## 레이어 구조 (앱 공통)

```
apps/{app_name}/
├── adapter/
│   ├── inbound/
│   │   ├── api/        # FastAPI 라우터, Pydantic 입력 스키마
│   │   ├── grpc/       # gRPC (선택)
│   │   └── websocket/  # WebSocket (선택)
│   └── outbound/
│       ├── orm/        # SQLAlchemy ORM 모델
│       └── pg/         # PostgreSQL 레포지토리 구현체
├── app/
│   ├── dtos/           # 레이어 간 데이터 전달 객체 (dataclass)
│   ├── ports/
│   │   ├── input/      # 유스케이스 포트 (ABC)
│   │   └── output/     # 레포지토리 포트 (ABC)
│   └── use_cases/      # 인터랙터 (비즈니스 로직)
├── domain/
│   ├── entities/       # 엔티티
│   └── value_objects/  # 값 객체
└── dependencies/       # FastAPI Depends 프로바이더
```

---

## 모듈 경로 규칙

### 앱 내부 import

`fastapi`와 `apps` 경로 세그먼트를 생략한다.  
`main.py`가 `/app`(fastapi 루트)과 `/app/apps`를 `sys.path`에 추가하기 때문이다.

```python
# 올바름
from titanic.adapter.inbound.api import titanic_router
from scout.adapter.inbound.api import scout_routers

# 틀림
from fastapi.apps.titanic.adapter.inbound.api import titanic_router
```

### core 모듈 import

`core.matrix.*` 경로를 직접 사용한다. re-export shim은 만들지 않는다.

```python
# 올바름
from core.matrix.grid_oracle_database_manager import get_db, get_engine
from core.matrix.vault_keymaker_secret_manager import generate_reply
from core.matrix.gird_neo_theone_base import Base

# 틀림
from core.database import get_db
from fastapi.core.database import get_db
```

---

## core/matrix 공유 인프라

| 파일 | 역할 |
|------|------|
| `grid_oracle_database_manager.py` | AsyncSession 팩토리, `get_db`, `get_engine`, `configure_engine`, `dispose_engine`, 테이블 생성 |
| `vault_keymaker_secret_manager.py` | Gemini API 클라이언트 (`generate_reply` 등) |
| `gird_neo_theone_base.py` | SQLAlchemy `DeclarativeBase` |
| `gird_morpheus_base_orchestrator.py` | 오케스트레이터 베이스 |
| `gird_smith_agent_scaler.py` | 에이전트 스케일러 |
| `grit_trinity_hacker_mixin.py` | 해커 믹스인 |
| `kiwi_oracle_morpheme_analyzer.py` | kiwipiepy 한국어 형태소 분석 |
| `ollama_neo_local_model.py` | Ollama 로컬 모델 클라이언트 |
| `chat_router.py` | `/chat` 엔드포인트 (Gemini 연동) |
| `vault_keymaker/` | 시크릿 관리 서브모듈 |

`core/matrix/__init__.py`는 비워 둔다. 각 모듈을 직접 import한다.

---

## 환경 변수 (`core/config.py`, `Settings`)

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `DATABASE_URL` | — | Neon PostgreSQL 연결 문자열 |
| `GEMINI_API_KEY` | — | Google Gemini API 키 |
| `NEXUS_API_KEY` | — | Nexus Mods API 키 |
| `STEAM_API_KEY` | — | Steam API 키 |
| `OLLAMA_BASE_URL` | `http://localhost:11434` | Ollama 서버 URL |
| `OLLAMA_MODEL` | `llama3.2` | Ollama 모델명 |

`get_settings()`는 `@lru_cache`로 싱글턴. FastAPI `Depends(get_settings)`로 주입한다.

---

## 앱 목록

| 앱 | 설명 | 등록 방식 |
|----|------|-----------|
| `titanic` | 타이타닉 승객 ML/데이터 파이프라인 | `app.include_router(titanic_router)` (+ `/api` prefix) |
| `scout` | 게임 장르 탐색·패치노트 번역 | `scout_routers` (복수 라우터) |
| `login` | 사용자 인증 (회원가입·로그인) | `friday13th_v1_routers` (복수 라우터) |
| `doro` | CSV 데이터 리더 | `GET /doro/data` |
| `adapters` | 공유 어댑터 (`DatabaseHealthAdapter`) | `GET /health/db` |
| `agora` | (확장 예정) | — |
| `inception` | (확장 예정) | — |
| `community` | (확장 예정) | — |
| `imitation_game` | (확장 예정) | — |

---

## 엔티티 / DB 규칙

모든 테이블 PK는 **`id` (int, 자동 증감)**으로 통일한다. 상세 규칙: `vault/DevOps/Backend/ENTITY_RULE.md`

```python
from typing import Optional
from sqlmodel import Field, SQLModel

class ExampleModel(SQLModel, table=True):
    __tablename__ = "examples"

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
```

- PK 이름: 반드시 `id`. `user_id`, `pk` 등 금지.
- FK 참조: `field_id: int = Field(foreign_key="table.id")`
- 비즈니스 식별자는 별도 컬럼 (`unique=True`, `index=True`)으로 분리.
- UUID PK 단독 사용 금지. surrogate int `id` 항상 포함.

---

## titanic 앱 — 캐릭터 역할 매핑

| 캐릭터 | URL prefix | 담당 |
|--------|-----------|------|
| James Cameron | `/james` | CSV 업로드, DB 적재 |
| Walter Nichols | `/walter` | 승객 명단 관리 |
| Rose DeWitt | `/rose` | ML 학습 데이터 전체 조회 |
| Ruth DeWitt | `/ruth` | 등급(pclass) 필터 조회 |
| Captain Smith | `/smith` | 전체 통계 (생존/사망) |
| Jack Dawson | `/jack` | 생존 예측 학습 데이터 |
| Caledon Hockley | `/cal` | 입력값 유효성 검사 |
| Thomas Andrews | `/andrews` | 아키텍처 레퍼런스 |
| Wallace Hartley | `/hartley` | 배경 작업 / 이벤트 스트리밍 |
| Isidor & Ida | `/isidor` | 커플 도메인 |
| Harold Lowe | `/lowe` | 구명보트 (복구 작업) |
| Molly Brown | `/molly` | 피처 스케일링 |

모든 캐릭터는 `GET /{prefix}/myself` 엔드포인트를 가진다.

---

## 네이밍 규칙

| 구성요소 | 패턴 | 예시 |
|---------|------|------|
| 라우터 변수명 | `{character}_router` | `james_director_router` |
| 유스케이스 포트 | `{Character}UseCase` | `JackUseCase` |
| 인터랙터 | `{Character}Interactor` | `JackInteractor` |
| pg 레포지토리 | `{Character}PgRepository` | `JackPgRepository` |
| DTO | `{Character}Query`, `{Character}Response` | `JackQuery` |
| Depends 프로바이더 | `get_{character}_use_case` | `get_jack_use_case` |

---

## 머신러닝 데이터 분석 원칙

### Categorical

데이터가 카테고리로 묶일 때 사용한다.

**nominal** : 이름을 바탕으로 하는 척도  
순서와는 상관없이 그냥 셀 수 있는 정도의 데이터  
ex) 청팀, 홍팀, 백팀

**ordinal** : 순서를 바탕으로 하는 척도  
자료들 사이에 순서(서열)가 있는 경우  
ex) 청팀이 이길 가능성 1. 매우 낮음 2. 낮음 3. 보통 4. 높음 5. 매우높음

### Quantitative

숫자로 셀 수 있을때 사용한다.

**interval** : 간격을 바탕으로 하는 척도  
기준이 없이 일정한 측정 구간을 갖는 데이터  
ex) 11:00~11:05, 온도, pH (10배 덥다·시다 불가능)

**ratio** : 비율을 바탕으로 하는 척도  
절대적 원점(0)을 기준으로 두는 데이터  
ex) 나이, 돈, 몸무게 (10배 많다 가능)

---

## async / sync 선택 기준

| 메소드 성격 | 형태 | 이유 |
|------------|------|------|
| I/O-bound (DB, LLM, 네트워크) | `async def` | 이벤트 루프를 블로킹하지 않기 위해 |
| CPU-bound (Kiwi 형태소 등) | `def` | await할 대상이 없고, async로 선언해도 블로킹은 동일 |

### CPU-bound 작업이 오래 걸릴 때

`async def`로 바꾸는 것이 아니라 호출 측에서 스레드풀로 넘긴다.

```python
import asyncio

result = await asyncio.to_thread(use_case.analyze_intent, question)
```

`async def`로 선언해도 `kiwi.tokenize()` 같은 동기 연산은 이��트 루프를 그대로 막는다.
표시만 비동기이고 실제로는 블로킹 — 오히려 더 나쁜 상황이 된다.
