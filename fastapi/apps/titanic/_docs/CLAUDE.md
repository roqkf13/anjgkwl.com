# Titanic 앱 지침

## 도메인 개요

타이타닉 승객·승무원 데이터를 기반으로 한 ML/데이터 파이프라인 앱.  
캐릭터별로 역할이 분리되며, 각 캐릭터가 하나의 기능 슬라이스를 담당한다.

---

## 캐릭터 → 역할 매핑

| 캐릭터 | prefix | 담당 |
|--------|--------|------|
| James Cameron | `/james` | CSV 업로드, DB 적재 |
| Walter Nichols | `/walter` | 승객 명단 관리 |
| Rose DeWitt Bukater | `/rose` | ML 학습 데이터 전체 조회 |
| Ruth DeWitt Bukater | `/ruth` | 등급(pclass) 필터 조회 |
| Captain Smith | `/smith` | 전체 통계 (생존/사망 수) |
| Jack Dawson | `/jack` | 생존 예측 모델 학습 데이터 |
| Caledon Hockley | `/cal` | 입력값 유효성 검사 |
| Thomas Andrews | `/andrews` | 설계자 (아키텍처 레퍼런스) |
| Wallace Hartley | `/hartley` | 배경 작업 / 이벤트 스트리밍 |
| Isidor & Ida Straus | `/isidor` | 커플 도메인 |
| Harold Lowe | `/lowe` | 구명보트 (복구 작업) |
| Molly Brown | `/molly` | 피처 스케일링 |

---

## 레이어 구조

```
titanic/
├── adapter/
│   ├── inbound/api/
│   │   ├── schemas/        # Pydantic 입력 스키마
│   │   └── v1/             # FastAPI 라우터
│   └── outbound/
│       ├── orm/            # SQLAlchemy ORM 모델
│       └── pg/             # PostgreSQL 레포지토리 구현체
├── app/
│   ├── dtos/               # 레이어 간 데이터 전달 객체 (dataclass)
│   ├── ports/
│   │   ├── input/          # 유스케이스 포트 (ABC)
│   │   └── output/         # 레포지토리 포트 (ABC)
│   └── use_cases/          # 인터렉터 (비즈니스 로직)
└── dependencies/           # FastAPI Depends 프로바이더
```

---

## DB 테이블

| 테이블 | ORM 별칭 | 주요 컬럼 |
|--------|----------|-----------|
| `titanic_person` | `JackTrainerOrm` as `PersonOrm` | `passenger_id`, `name`, `gender`, `age`, `survived` |
| `titanic_booking` | `RoseModelOrm` as `BookingOrm` | `passenger_id`, `pclass`, `ticket`, `fare`, `cabin`, `embarked` |

조인 기준: `BookingOrm.passenger_id == PersonOrm.passenger_id`

---

## 네이밍 규칙

- 라우터 변수명: `{character}_router` (예: `james_director_router`)
- 유스케이스 포트: `{Character}UseCase`
- 인터렉터: `{Character}Interactor`
- pg 레포지토리: `{Character}PgRepository`
- DTO Query/Response: `{Character}Query`, `{Character}Response`
- 프로바이더 함수: `get_{character}_use_case`

---

## introduce_myself 규칙

모든 캐릭터는 `GET /{prefix}/myself` 엔드포인트를 가진다.  
pg 레포지토리 mock 응답 형식: `id=query.id * 10000, name=query.name + "가 레포지토리에 다녀옴"`


## 타이타닉 도메인 문서 연결


- 타이타닉 도메인 문서 연결
- 타이타닉 피처 정리 : [[titanic-features]]
- 타이타닉 머신러닝 : [[titanic-machine-learning]]
- 타이타닉 ERD : [[titanic-erd]]
- 타이타닉 NF : [[titanic-nf]]
- 타이타닉 알고리즘 : [[titanic-algorithm]]
- Backend 전체 지침 : [[fastapi/CLAUDE|Backend 전체 지침]]
