# Entity / 테이블 규칙 (Cursor / 에이전트용)

이 문서는 백엔드(`backend/apps/**` 등)에서 **SQLModel 엔티티·Alembic 마이그레이션**을 작성할 때 Cursor에서 `@docs/DevOps/Backend/ENTITY_RULE.md` 로 참조한다.

---

## 1. 기본 키(PK)는 `id` (int, 자동 증감)

- 이 프로젝트의 **모든 테이블**은 시스템 내부용 **정수형 자동 증감 고유 번호**를 기본 키로 갖는다.
- **필드명·DB 컬럼명 모두 `id`로 통일**한다. (`user_id`, `order_id`, `pk` 등을 PK 이름으로 쓰지 않는다.)
- 타입은 **`int`** (PostgreSQL: `INTEGER` / `SERIAL` 계열, Alembic autogenerate 시 autoincrement).
- ORM 모델에서는 **`Optional[int]`** + `default=None` + `primary_key=True` 패턴을 사용한다.

### 표준 필드 정의 (참조 구현)

```python
from typing import Optional

from sqlmodel import Field, SQLModel


class Example(SQLModel, table=True):
    __tablename__ = "examples"

    # 1. 시스템 내부용 자동 증가 고유 번호 (기본 키)
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},  # DB 컬럼명: id
    )
```

### 프로젝트 내 예시

- `backend/apps/secom/app/models/user_entity.py` — `User.id`

---

## 2. 비즈니스 식별자와 `id` 구분

- **PK `id`**: DB·ORM 내부 조인·FK·페이지네이션용. 사용자에게 노출하지 않아도 됨.
- **비즈니스 식별자** (예: `user_id`, `order_no`, `email`): PK가 아닌 **별도 컬럼**으로 둔다. 필요 시 `unique=True`, `index=True`.
- FK 참조 시 **항상 `id`(int)** 를 가리킨다. (`user_id` 문자열 컬럼을 FK 타깃으로 쓰지 않는다.)

```python
class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        sa_column_kwargs={"name": "id"},
    )
    user_id: int = Field(foreign_key="users.id", index=True)  # FK → users.id
    order_no: str = Field(max_length=64, unique=True, index=True)  # 비즈니스 번호
```

---

## 3. 비권장

```python
# PK 이름이 id 가 아님
user_id: str = Field(primary_key=True)

# UUID 를 PK 로만 두고 int id 가 없음
id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

# 복합 PK 만 있고 surrogate id 가 없음 (예외 없으면 금지)
```

---

## 4. Alembic · DB

- 새 테이블 생성 시 `id` 컬럼: `sa.Integer()`, `autoincrement=True`, `primary_key=True`.
- 기존 테이블에 PK 이름이 `id`가 아니면 **마이그레이션으로 `id` int PK 추가·통일**을 검토한다.
- `python -m alembic revision --autogenerate` 후 생성된 migration에서 `id` 정의가 위 규칙과 맞는지 확인한다.

---

## 5. Cursor에 붙여 넣을 프롬프트 (복사용)

```text
@docs/DevOps/Backend/ENTITY_RULE.md

SQLModel 엔티티를 만들어줘.
- 모든 테이블 PK: int 자동 증감, 필드명·컬럼명 id
- id: Optional[int] = Field(default=None, primary_key=True, sa_column_kwargs={"name": "id"})
- 비즈니스 식별자는 id 와 별도 컬럼
```

### 짧은 버전

```text
@docs/DevOps/Backend/ENTITY_RULE.md 적용해서 이 엔티티/마이그레이션 작성해줘. PK는 int id.
```

---

## 6. 에이전트 체크리스트

엔티티·마이그레이션 작성 후 스스로 확인:

- [ ] PK 필드명이 **`id`** 인가?
- [ ] PK 타입이 **`int`** (자동 증감) 인가?
- [ ] `sa_column_kwargs={"name": "id"}` 로 DB 컬럼명이 **`id`** 인가?
- [ ] 비즈니스용 `user_id` / `order_no` 등을 PK로 쓰지 않았는가?
- [ ] FK는 **`…_id: int = Field(foreign_key="…table.id")`** 형태인가?
