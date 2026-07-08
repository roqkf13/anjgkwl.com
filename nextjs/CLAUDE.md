# www — 프론트엔드 프로젝트

Next.js 기반 웹 앱. 일반 지침은 루트 `CLAUDE.md` 참조.

## 기술 스택

- **Next.js 16 (App Router)** + **React 19** + **TypeScript 5.7**
- **Tailwind CSS v4** + shadcn/ui (Radix UI 기반)
- **React Hook Form** + **Zod** (폼 검증)
- **Google Generative AI** (Gemini API)
- 패키지 매니저: **pnpm**

## 디렉토리 구조

```
www/
└── v0-titanic-qa-app/   ← 실제 Next.js 앱 루트
    ├── app/             ← App Router (pages + API routes)
    │   ├── api/gemini/  ← Gemini 채팅 API route
    │   ├── admin/  chat/  lesson/  login/  scout/  signup/  titanic/
    │   └── layout.tsx  page.tsx
    ├── components/      ← UI 컴포넌트 (shadcn/ui 기반)
    ├── hooks/           ← 커스텀 훅
    └── lib/             ← 유틸리티 (API 클라이언트 등)
```

## 개발 / 빌드

```bash
# www/ 루트에서 실행
npm run dev        # webpack (안정)
npm run dev:turbo  # Turbopack (빠름, 실험적)
npm run build
npm run lint
```

## 컨벤션

- 서버 컴포넌트를 기본값으로. `"use client"`는 인터랙션이 필요한 곳에만.
- 새 UI 컴포넌트는 shadcn/ui 패턴 (`components/ui/`).
- API route는 `app/api/` 안에 `route.ts`로 작성.
