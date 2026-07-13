# [Claude Code 작업 지시서] pgvector DB 테이블 생성 (Alembic)

> 본 문서는 Karpathy의 하네스(Harness) 원칙 — **목표 명시 → 컨텍스트 제공 → 제약조건 명시 → 검증 기준 제시 → 단계적 실행** — 에 따라 작성된 Claude Code용 프롬프트입니다.
> 이 파일 전체를 Claude Code에 그대로 붙여넣어 실행하세요.

---

## 0. 역할 정의 (Role)

너는 PostgreSQL(pgvector 확장 포함) + Alembic 마이그레이션 전문가야.
아래 ERD를 기반으로 Alembic 마이그레이션 스크립트를 작성하고, 실제로 마이그레이션을 실행해서 테이블이 정상 생성되는 것까지 검증해줘.

---

## 1. 환경 정보 (Context)

- OS: Ubuntu 26
- DB: PostgreSQL + pgvector extension → **Docker 컨테이너 내부에서 실행** (호스트에 직접 설치 금지)
- 마이그레이션 도구: Alembic (SQLAlchemy 기반, 호스트 또는 별도 앱 컨테이너에서 실행)
- 프로젝트 구조: 현재 디렉토리 기준 `alembic.ini`, `alembic/` 폴더가 이미 존재한다고 가정. 없다면 `alembic init alembic`부터 실행할 것.
- DB 접속 정보는 `.env` 또는 `alembic/env.py` 내 `SQLALCHEMY_DATABASE_URL` / `DATABASE_URL` 환경변수를 참조. 하드코딩 금지.

---

## 1-1. Docker 기반 DB 설치 (Docker DB Setup)

DB는 호스트에 직접 설치하지 않고, Docker 컨테이너로 띄운다.

### 요구사항
- pgvector 확장이 사전 설치된 이미지 사용: `pgvector/pgvector:pg16` (또는 프로젝트에서 사용 중인 PostgreSQL 메이저 버전에 맞는 태그. 버전 미지정 시 `pg16` 사용)
- `docker-compose.yml` (또는 기존 파일이 있다면 그것을 수정)에 아래 내용 포함:
  - 서비스명: `db` (또는 기존 컨벤션이 있다면 그에 맞출 것)
  - 이미지: `pgvector/pgvector:pg16`
  - 환경변수: `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` — `.env` 파일에서 값을 읽어오도록 구성 (하드코딩 금지)
  - 포트 매핑: `5432:5432` (충돌 시 호스트 포트만 변경, 컨테이너 내부 포트는 5432 유지)
  - 볼륨: named volume으로 데이터 영속화 (예: `pgdata:/var/lib/postgresql/data`)
  - `healthcheck`: `pg_isready` 기반으로 DB 준비 상태 확인
- Alembic이 컨테이너 내부 DB에 접속할 수 있도록 `DATABASE_URL`은 `postgresql://<user>:<pass>@localhost:5432/<db>` 형태로 `.env`에 구성 (Alembic을 호스트에서 실행한다는 전제. 만약 Alembic도 컨테이너에서 실행할 경우 host는 서비스명 `db`로 대체)

### 실행 절차
1. `docker-compose.yml` 작성 또는 수정 (기존 파일 있으면 백업 후 diff로 보여줄 것)
2. `docker compose up -d db` 로 컨테이너 기동
3. `docker compose ps` 및 `healthcheck` 상태로 컨테이너가 `healthy` 될 때까지 대기
4. 컨테이너 내부에서 pgvector 확장이 실제로 설치돼 있는지 확인:
   ```
   docker compose exec db psql -U <user> -d <db> -c "\dx"
   ```
   결과에 `vector` extension이 없다면 아래를 실행:
   ```
   docker compose exec db psql -U <user> -d <db> -c "CREATE EXTENSION IF NOT EXISTS vector;"
   ```
5. 이후 섹션 4(Alembic 작업 순서)를 진행하되, 모든 `alembic upgrade/downgrade` 명령은 컨테이너가 `healthy` 상태인지 먼저 확인한 뒤 실행할 것.

### 제약사항 (Docker 관련)
- 기존에 실행 중인 DB 컨테이너나 볼륨을 임의로 삭제하지 말 것 (특히 `docker compose down -v`는 사용자 승인 없이 실행 금지).
- 포트가 이미 사용 중이면 임의로 다른 서비스를 종료하지 말고, 호스트 포트 매핑만 조정한 뒤 사용자에게 보고할 것.
- 이미지 태그(`pg16` 등)는 프로젝트의 기존 PostgreSQL 버전과 다를 경우 반드시 먼저 확인 후 맞출 것.

---

## 2. ERD 명세 (Schema Spec)

아래 4개 테이블을 생성한다. 컬럼명, 타입, PK/FK, 길이 제약을 정확히 반영할 것.

### 2-1. stadium
| 컬럼 | 타입 | 제약 |
|---|---|---|
| stadium_id | VARCHAR(10) | PK |
| statdium_name | VARCHAR(40) | |
| hometeam_id | VARCHAR(10) | |
| seat_count | INTEGER | |
| address | VARCHAR(60) | |
| ddd | VARCHAR(10) | |
| tel | VARCHAR(10) | |

### 2-2. team
| 컬럼 | 타입 | 제약 |
|---|---|---|
| team_id | VARCHAR(10) | PK |
| region_name | VARCHAR(10) | |
| team_name | VARCHAR(40) | |
| e_team_name | VARCHAR(50) | |
| orig_yyyy | VARCHAR(10) | |
| zip_code1 | VARCHAR(10) | |
| zip_code2 | VARCHAR(10) | |
| address | VARCHAR(80) | |
| ddd | VARCHAR(10) | |
| tel | VARCHAR(10) | |
| fax | VARCHAR(10) | |
| homepage | VARCHAR(50) | |
| owner | VARCHAR(10) | |
| stadium_id | VARCHAR(10) | FK → stadium.stadium_id (nullable) |

### 2-3. player
| 컬럼 | 타입 | 제약 |
|---|---|---|
| player_id | VARCHAR(10) | PK |
| player_name | VARCHAR(20) | |
| e_player_name | VARCHAR(40) | |
| nickname | VARCHAR(30) | |
| join_yyyy | VARCHAR(10) | |
| position | VARCHAR(10) | |
| back_no | INTEGER | |
| nation | VARCHAR(20) | |
| birth_date | DATE | |
| solar | VARCHAR(10) | |
| height | INTEGER | |
| weight | INTEGER | |
| team_id | VARCHAR(10) | FK → team.team_id (nullable) |

### 2-4. schedule
| 컬럼 | 타입 | 제약 |
|---|---|---|
| sche_date | VARCHAR(10) | PK (복합키) |
| stadium_id | VARCHAR(10) | PK (복합키), FK → stadium.stadium_id |
| gubun | VARCHAR(10) | |
| hometeam_id | VARCHAR(10) | |
| awayteam_id | VARCHAR(10) | |
| home_score | INTEGER | |
| away_score | INTEGER | |

**참고**: `schedule`의 PK는 `sche_date` + `stadium_id` 복합키(ERD 상 두 컬럼 모두 열쇠 아이콘)로 처리할 것.

---

## 3. 관계 (Relationships)

- `stadium (1) --- (0..N) schedule` : `schedule.stadium_id` → `stadium.stadium_id`
- `stadium (1) --- (0..N) team` : `team.stadium_id` → `stadium.stadium_id`
- `team (1) --- (0..N) player` : `player.team_id` → `team.team_id`

모든 FK는 `ON DELETE SET NULL, ON UPDATE CASCADE`로 설정 (단, `schedule.stadium_id`는 복합 PK의 일부이므로 `ON DELETE RESTRICT` 적용).

---

## 4. 작업 순서 (Execution Steps)

0. (섹션 1-1 참고) `docker-compose.yml`로 pgvector 포함 PostgreSQL 컨테이너를 기동하고 `healthy` 상태 및 `vector` extension 설치를 확인.
1. 현재 디렉토리에 `alembic.ini`, `alembic/env.py`가 있는지 확인. 없으면 `alembic init alembic` 실행 후 `env.py`에 (컨테이너 DB를 가리키는) DB URL 연결 설정.
2. pgvector 확장이 활성화되어 있는지 확인하는 마이그레이션(`CREATE EXTENSION IF NOT EXISTS vector;`)을 별도 revision으로 먼저 생성. (현재 ERD 테이블 자체는 vector 컬럼을 쓰지 않지만, 추후 확장을 대비해 extension 활성화 리비전을 선행 배치. 컨테이너에서 이미 생성했더라도 마이그레이션 코드로도 명시해 재현성 확보)
3. 아래 순서로 Alembic revision을 생성 (FK 의존성 순서를 반드시 지킬 것):
   - `0001_create_stadium_table`
   - `0002_create_team_table`
   - `0003_create_player_table`
   - `0004_create_schedule_table`
4. 각 revision 파일의 `upgrade()`에는 `op.create_table(...)`로 테이블 생성, `downgrade()`에는 `op.drop_table(...)`로 롤백 로직을 작성.
5. (컨테이너가 `healthy` 상태인지 재확인 후) `alembic upgrade head`를 실행하여 실제로 테이블이 생성되는지 확인.
6. `docker compose exec db psql -U <user> -d <db> -c "\d <table>"` 형태로 컨테이너 내부 DB에 접속하여 `stadium`, `team`, `player`, `schedule` 결과를 출력해서 컬럼/타입/PK/FK가 명세와 일치하는지 검증.
7. `alembic downgrade -1`을 1회 실행해 최신 리비전이 정상적으로 롤백되는지도 확인 후, 다시 `alembic upgrade head`로 원복.

---

## 5. 제약사항 (Constraints)

- SQLAlchemy Core 스타일(`op.create_table`)을 사용할 것. ORM 모델 클래스는 별도로 요청하지 않는 한 만들지 말 것.
- 컬럼 타입은 ERD에 명시된 길이를 정확히 지킬 것 (예: `VARCHAR(40)`을 임의로 `VARCHAR(255)`로 바꾸지 말 것).
- 기존 마이그레이션 파일이나 DB 스키마를 임의로 삭제하지 말 것. 충돌 시 먼저 사용자에게 보고할 것.
- `.env`나 DB 접속 정보에 포함된 비밀번호 등 민감 정보를 로그나 커밋 메시지에 노출하지 말 것.

---

## 6. 완료 기준 (Definition of Done)

- [ ] DB 컨테이너가 `docker compose ps` 기준 `healthy` 상태이고 `vector` extension이 설치되어 있음
- [ ] 4개 테이블이 모두 생성되고 `\d` 결과가 ERD 명세와 100% 일치
- [ ] FK 제약조건이 정상적으로 걸려 있음 (`information_schema.table_constraints`로 확인)
- [ ] `alembic upgrade head` / `alembic downgrade -1` 왕복 테스트 통과
- [ ] 생성된 마이그레이션 파일 목록과 각 파일의 핵심 diff를 최종 요약으로 보고

---

## 7. 보고 형식 (Output Format)

작업 완료 후 아래 형식으로 요약 보고할 것:

```
✅ Docker DB 컨테이너 상태: [healthy 여부 / vector extension 설치 여부]
✅ 생성된 revision 파일: [파일명 리스트]
✅ 테이블 생성 결과: [각 테이블 컬럼 수 / PK / FK 확인 결과]
✅ upgrade/downgrade 테스트 결과: [통과/실패]
⚠️ 발견된 이슈 또는 ERD와 다르게 처리한 부분 (있다면)
```
