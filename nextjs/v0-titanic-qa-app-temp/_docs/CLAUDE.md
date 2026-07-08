# Frontend (www) 지침

## 프로젝트 개요

- **런타임**: Node.js, Next.js 15 (App Router), TypeScript
- **실제 앱 경로**: `www/v0-titanic-qa-app/`
- **포트**: 3000
- **UI 라이브러리**: shadcn/ui + Radix UI + Tailwind CSS
- **폰트**: Geist, Geist Mono (Google Fonts)
- **분석**: Vercel Analytics (`@vercel/analytics/next`)
- **백엔드 연동**: Docker Compose 내부망 → abiswallow (포트 8000)
- **패키지 매니저**: pnpm (`pnpm-lock.yaml`)

---

## 디렉터리 구조

```
www/
└── v0-titanic-qa-app/
    ├── app/                        # Next.js App Router 루트
    │   ├── api/
    │   │   └── gemini/             # Gemini Route Handler
    │   ├── chat/                   # Gemini 채팅 페이지
    │   ├── lesson/                 # 레슨 레이아웃 + 타이타닉 서브페이지
    │   │   └── titanic/
    │   ├── login/                  # 로그인
    │   ├── signup/                 # 회원가입
    │   ├── scout/
    │   │   └── [genre]/            # 장르별 허브 (동적 라우트)
    │   │       ├── metroidvania/
    │   │       ├── openworld/
    │   │       ├── roguelike/
    │   │       └── soulslike/
    │   ├── titanic/                # 타이타닉 ML 대시보드
    │   ├── globals.css
    │   ├── layout.tsx              # 루트 레이아웃 (AppNavBar 포함)
    │   └── page.tsx                # 홈
    ├── components/
    │   ├── ui/                     # shadcn/ui 기본 컴포넌트
    │   ├── app-nav-bar.tsx
    │   ├── auth-page-shell.tsx
    │   ├── gemini-chat.tsx
    │   ├── lesson-category-nav.tsx
    │   ├── lesson-layout-shell.tsx
    │   ├── lesson-side-nav.tsx
    │   ├── scout-collected-games.tsx
    │   ├── scout-favorite-genres-panel.tsx
    │   ├── scout-game-card.tsx
    │   ├── scout-game-detail-view.tsx
    │   ├── scout-game-search.tsx
    │   ├── scout-genre-hub.tsx
    │   ├── scout-genre-hub-body.tsx
    │   ├── scout-genre-hub-header.tsx
    │   ├── scout-patch-note-modal.tsx
    │   ├── scout-zones.tsx
    │   ├── theme-provider.tsx
    │   ├── titanic-lesson-aside.tsx
    │   ├── titanic-neon-sidebar.tsx
    │   └── titanic-upload-panel.tsx
    ├── lib/
    │   ├── scout-game-detail.ts    # 게임 상세 데이터 유틸
    │   ├── scout-game-lookup.ts    # 게임 조회 유틸
    │   ├── scout-genres.ts         # 장르 상수 (ScoutGenre, ScoutGame 타입)
    │   ├── scout-merged-genres.ts  # 병합 장르 데이터
    │   └── utils.ts                # cn() 등 공통 유틸
    ├── hooks/
    │   ├── use-mobile.ts           # 모바일 감지
    │   └── use-toast.ts            # 토스트 훅
    └── styles/
```

---

## 페이지 목록

| 경로 | 설명 |
|------|------|
| `/` | 홈 |
| `/login` | 로그인 (`friday13th` 백엔드) |
| `/signup` | 회원가입 (`friday13th` 백엔드) |
| `/chat` | Gemini 채팅 (`/api/gemini` Route Handler 경유) |
| `/lesson` | 레슨 레이아웃 |
| `/lesson/titanic` | 타이타닉 레슨 |
| `/titanic` | 타이타닉 ML 데이터 대시보드 |
| `/scout/[genre]` | 장르 허브 (soulslike, roguelike, openworld, metroidvania) |

---

## 주요 컴포넌트

| 파일 | 역할 |
|------|------|
| `app-nav-bar.tsx` | 루트 레이아웃에 포함되는 상단 내비게이션 |
| `auth-page-shell.tsx` | 로그인/회원가입 공통 껍데기 |
| `gemini-chat.tsx` | Gemini 채팅 UI (`/api/gemini` 연동) |
| `lesson-layout-shell.tsx` | 레슨 레이아웃 (사이드바 + 컨텐츠) |
| `lesson-side-nav.tsx` | 레슨 사이드 내비게이션 |
| `lesson-category-nav.tsx` | 카테고리 내비게이션 |
| `scout-genre-hub.tsx` | 장르 허브 최상위 컴포넌트 |
| `scout-genre-hub-header.tsx` | 장르 허브 헤더 |
| `scout-genre-hub-body.tsx` | 장르 허브 본문 |
| `scout-game-card.tsx` | 게임 카드 |
| `scout-game-detail-view.tsx` | 게임 상세 뷰 |
| `scout-game-search.tsx` | 게임 검색 |
| `scout-patch-note-modal.tsx` | 패치노트 모달 (번역 포함) |
| `scout-collected-games.tsx` | 수집된 게임 목록 |
| `scout-favorite-genres-panel.tsx` | 즐겨찾기 장르 패널 |
| `scout-zones.tsx` | 스카우트 존 레이아웃 |
| `titanic-neon-sidebar.tsx` | 타이타닉 네온 사이드바 |
| `titanic-lesson-aside.tsx` | 타이타닉 레슨 보조 패널 |
| `titanic-upload-panel.tsx` | 타이타닉 CSV 업로드 패널 |
| `theme-provider.tsx` | 다크/라이트 테마 프로바이더 |

---

## 규칙

### 컴포넌트

- `app/` 디렉터리 기준 App Router 구조를 따른다.
- 서버 컴포넌트와 클라이언트 컴포넌트를 명확히 구분한다 (`"use client"` 명시).
- 스타일은 Tailwind CSS + shadcn/ui를 사용한다. 임의로 방식을 바꾸지 않는다.
- shadcn/ui 기본 컴포넌트는 `components/ui/`에, 도메인 컴포넌트는 `components/` 루트에 둔다.

### API 호출

- `fetch`를 직접 쓰거나 전용 클라이언트 모듈(`lib/`)로 분리한다.
- 컴포넌트 안에 URL을 하드코딩하지 않는다.
- 환경변수는 `NEXT_PUBLIC_` 접두사 규칙을 지킨다.
- Gemini 호출은 클라이언트에서 직접 하지 않고 `/api/gemini` Route Handler를 경유한다.

### useState — 적게, 객체로

폼 입력값은 `useState`로 들고 있지 않고 `FormData`로 읽는다.  
UI 플래그(`error`, `loading`, `success`)는 하나의 객체 `useState`로 묶는다.

```tsx
type UiState = { error: string | null; success: boolean; submitting: boolean };
const [ui, setUi] = useState<UiState>({ error: null, success: false, submitting: false });

const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(e.currentTarget).entries());
  setUi((prev) => ({ ...prev, submitting: true }));
  try {
    // fetch(...)
    setUi((prev) => ({ ...prev, success: true }));
  } catch {
    setUi((prev) => ({ ...prev, error: "오류가 발생했습니다." }));
  } finally {
    setUi((prev) => ({ ...prev, submitting: false }));
  }
};
```

### 민감 정보 노출 금지

- `window.alert` / `console.log`에 폼 입력값(이름, 이메일, 비밀번호)을 넣지 않는다.
- 서버 `detail` 응답을 그대로 사용자에게 노출하지 않는다.

---

## 개발 서버 실행

```bash
# www/ 루트에서
npm run dev        # webpack 모드 (포트 3000)
npm run dev:turbo  # turbopack 모드
```

스크립트는 `v0-titanic-qa-app/`을 `--prefix`로 실행한다.

---

## 참고 문서

- `vault/DevOps/Frontend/REACT_RULES.md` — useState/FormData 패턴 상세

## 다크 모드

명세: [darkmode_spec.md](./v0-titanic-qa-app/_docs/darkmode_spec.md)