import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_APPS = _ROOT / "apps"
for _p in (_ROOT, _APPS):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from fastapi import FastAPI

from auth.router import auth_router

app = FastAPI(
    title="RAG Tailor Auth",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,  # 실서비스: 문서 비노출
)
# auth.anjgkwl.com 자체가 이미 인증 전용 서브도메인이라, /auth 접두사를 또 붙이면
# auth.anjgkwl.com/auth/login처럼 중복돼서 접두사 없이 마운트한다.
app.include_router(auth_router)


@app.get("/healthz")
async def healthz() -> dict[str, bool]:
    return {"ok": True}
