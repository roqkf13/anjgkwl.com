---
type: hub
id: star_craft
title: "Star Craft Hub — Graph·Vector DB 라이프라인 전략"
links:
  - friday13th
  - scout
  - titanic
  - doro
---

# Star Craft Hub — Graph·Vector DB 라이프라인 전략

## 1. 전제: 허브가 DB 라이프라인을 독점하는 이유

스타 토폴로지에서 스포크(spoke)는 서로를 직접 알면 안 된다.
그래프 DB와 벡터 DB는 **스포크 간 관계 정보**와 **의미 검색 인덱스**를 담기 때문에,
이 두 DB에 대한 접속 라이프라인은 **허브(star_craft)만** 소유한다.

```
스포크 A ──▶ hub (star_craft) ──▶ Neo4j   (관계 그래프)
스포크 B ──▶ hub (star_craft) ──▶ Qdrant  (벡터 인덱스)
```

스포크가 그래프/벡터 정보가 필요하면 허브 포트(Port)를 통해 요청한다.

---

## 2. 선택 DB

| 역할 | 서비스 | 이유 |
|------|--------|------|
| 그래프 DB | **Neo4j 5 (Community)** | Cypher 쿼리, Python `neo4j` 드라이버 안정, 도커 공식 이미지 |
| 벡터 DB | **Qdrant** | REST + gRPC, `qdrant-client` Python SDK, 경량 단일 컨테이너 |

---

## 3. docker-compose.yaml 추가 서비스

```yaml
services:
  # --- 기존 서비스 유지 ---

  neo4j:
    image: neo4j:5-community
    ports:
      - "7474:7474"   # Browser UI
      - "7687:7687"   # Bolt (Python 드라이버)
    environment:
      - NEO4J_AUTH=neo4j/${NEO4J_PASSWORD}
    volumes:
      - neo4j_data:/data

  qdrant:
    image: qdrant/qdrant:latest
    ports:
      - "6333:6333"   # REST API
      - "6334:6334"   # gRPC
    volumes:
      - qdrant_data:/qdrant/storage

volumes:
  neo4j_data:
  qdrant_data:
  n8n_data:   # 기존
```

환경변수 (`abiswallow/.env`):

```dotenv
NEO4J_URI=bolt://neo4j:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=changeme

QDRANT_HOST=qdrant
QDRANT_PORT=6333
```

> 로컬 직접 실행(도커 밖)에서는 `neo4j:7687` → `localhost:7687`,
> `qdrant` → `localhost`로 바꿔 사용.

---

## 4. 허브 내 아키텍처 (헥사고날)

```
apps/star_craft/
├── adapter/
│   └── outbound/
│       ├── graph/
│       │   ├── neo4j_client.py          ← 싱글턴 드라이버, 세션 컨텍스트
│       │   └── graph_repository.py      ← Cypher 쿼리 래핑
│       └── vector/
│           ├── qdrant_client.py         ← 싱글턴 QdrantClient
│           └── vector_repository.py     ← 컬렉션 생성·검색·업서트
├── app/
│   └── ports/
│       └── output/
│           ├── graph_port.py            ← 추상 인터페이스 (Protocol)
│           └── vector_port.py           ← 추상 인터페이스 (Protocol)
└── dependencies/
    └── db.py                            ← FastAPI Depends 주입 팩토리
```

### 4-1. Graph Port (Protocol)

```python
# app/ports/output/graph_port.py
from typing import Protocol

class GraphPort(Protocol):
    async def upsert_node(self, label: str, props: dict) -> None: ...
    async def upsert_edge(self, src: str, dst: str, rel: str, props: dict | None = None) -> None: ...
    async def query(self, cypher: str, params: dict | None = None) -> list[dict]: ...
```

### 4-2. Vector Port (Protocol)

```python
# app/ports/output/vector_port.py
from typing import Protocol

class VectorPort(Protocol):
    async def upsert(self, collection: str, id: str, vector: list[float], payload: dict) -> None: ...
    async def search(self, collection: str, vector: list[float], top_k: int = 5) -> list[dict]: ...
```

### 4-3. 클라이언트 싱글턴 패턴

```python
# adapter/outbound/graph/neo4j_client.py
import os
from functools import lru_cache
from neo4j import AsyncGraphDatabase, AsyncDriver

@lru_cache
def get_neo4j_driver() -> AsyncDriver:
    return AsyncGraphDatabase.driver(
        os.environ["NEO4J_URI"],
        auth=(os.environ["NEO4J_USER"], os.environ["NEO4J_PASSWORD"]),
    )

# adapter/outbound/vector/qdrant_client.py
import os
from functools import lru_cache
from qdrant_client import AsyncQdrantClient

@lru_cache
def get_qdrant_client() -> AsyncQdrantClient:
    return AsyncQdrantClient(
        host=os.getenv("QDRANT_HOST", "localhost"),
        port=int(os.getenv("QDRANT_PORT", "6333")),
    )
```

---

## 5. 라이프라인 흐름 (요청 경로)

```
[스포크 유스케이스]
      │  HTTP / 내부 함수 호출
      ▼
[star_craft 유스케이스]
      │  GraphPort / VectorPort (추상)
      ▼
[star_craft outbound 어댑터]
      │  neo4j AsyncDriver  /  AsyncQdrantClient
      ▼
[Docker: neo4j:7687 / qdrant:6333]
```

스포크는 star_craft의 **inbound API(라우터)** 또는 **내부 포트 함수**를 호출한다.
직접 DB 드라이버를 import하지 않는다.

---

## 6. 의존성 패키지

```toml
# pyproject.toml 또는 requirements.txt
neo4j>=5.0          # AsyncGraphDatabase
qdrant-client>=1.9  # AsyncQdrantClient
```

---

## 7. 구현 순서 (체크리스트)

- [ ] `docker-compose.yaml` — neo4j, qdrant 서비스 추가 및 볼륨 선언
- [ ] `abiswallow/.env` — 4개 환경변수 추가
- [ ] `adapter/outbound/graph/neo4j_client.py` — 드라이버 싱글턴
- [ ] `adapter/outbound/graph/graph_repository.py` — upsert_node / upsert_edge / query 구현
- [ ] `adapter/outbound/vector/qdrant_client.py` — 클라이언트 싱글턴
- [ ] `adapter/outbound/vector/vector_repository.py` — upsert / search 구현
- [ ] `app/ports/output/graph_port.py` — Protocol 정의
- [ ] `app/ports/output/vector_port.py` — Protocol 정의
- [ ] `dependencies/db.py` — FastAPI `Depends` 팩토리 (그래프·벡터 리포지토리 주입)
- [ ] 단위 테스트: 리포지토리를 mock으로 교체하여 포트 계약 검증
