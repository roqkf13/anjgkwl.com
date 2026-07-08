# 1. Node.js 환경 시작
FROM node:24.15.0-alpine

# 2. 컨테이너 내부 작업 폴더 지정
WORKDIR /app

# 3. pnpm 활성화 (pnpm-lock.yaml lockfileVersion 9.0 → pnpm 9)
RUN corepack enable && corepack prepare pnpm@9 --activate

# 4. 의존성 파일만 먼저 복사 → 소스 변경 시 install 레이어 캐시 재사용
COPY v0-titanic-qa-app/package.json v0-titanic-qa-app/pnpm-lock.yaml ./v0-titanic-qa-app/

# 5. 의존성 설치
RUN pnpm -C ./v0-titanic-qa-app install

# 6. 나머지 소스 코드 복사
COPY . .

# 7. 프론트엔드 서버 실행
CMD ["pnpm", "-C", "./v0-titanic-qa-app", "run", "dev"]
