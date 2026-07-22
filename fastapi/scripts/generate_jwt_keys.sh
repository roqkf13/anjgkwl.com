#!/usr/bin/env bash
set -euo pipefail

openssl genrsa -out jwt_private.pem 2048
openssl rsa -in jwt_private.pem -pubout -out jwt_public.pem

echo
echo "아래 값을 base64 한 줄로 인코딩해 각 .env 파일에 넣으세요:"
echo "  base64 -w0 jwt_private.pem   → fastapi/.env.auth 의 JWT_PRIVATE_KEY_B64"
echo "  base64 -w0 jwt_public.pem    → fastapi/.env.auth 와 fastapi/.env 양쪽의 JWT_PUBLIC_KEY_B64"
echo
echo "jwt_private.pem, jwt_public.pem 파일 자체는 저장소에 커밋하지 마세요 (.gitignore 확인)."
