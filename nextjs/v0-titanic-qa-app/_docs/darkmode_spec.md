# 다크 모드 명세

## 동작 방식

- 라이브러리: `next-themes`
- 기본값: `dark` (앱 실행 시 다크 모드로 시작)
- 전략: `class` — `<html>` 태그에 `.dark` 클래스를 부착해 Tailwind의 `dark:` 변형 활성화
- 시스템 설정 감지: `enableSystem: false` (시스템 설정 무시, 항상 기본값 적용)

## 토글

- 위치: `AppNavBar` 우측
- 아이콘: `Sun` (라이트) / `Moon` (다크) — lucide-react
- 컴포넌트: `components/dark-mode-toggle.tsx` (클라이언트 컴포넌트)

## CSS 변수

`globals.css`에 `:root`(라이트)와 `.dark`(다크) 두 세트가 정의돼 있다.  
Tailwind `@custom-variant dark (&:is(.dark *))` 로 `.dark` 클래스 기반 변형을 활성화한다.

## 적용 범위

`layout.tsx`의 `<ThemeProvider>`가 전체 앱을 감싸므로 모든 페이지에 일괄 적용된다.
