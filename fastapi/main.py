import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
_APPS = _ROOT / "apps"
for _p in (_ROOT, _APPS):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import secrets

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from adapters.db_health_adapter import DatabaseHealthAdapter, get_db_health_adapter
from core.config import get_settings
from core.dependencies import RoleChecker
from core.security import Role
from core.matrix.chat_router import router as chat_router
from core.matrix.grid_oracle_database_manager import (
    configure_engine,
    create_titanic_tables,
    dispose_engine,
    get_db,
    get_engine,
)
from login.adapter.inbound.api.v1 import friday13th_v1_routers
from login.adapter.outbound.orm.user_model import Base as Friday13thBase
from scout.adapter.inbound.api import scout_routers
from community.adapter.inbound.api import community_router
from admin.adapter.inbound.api import admin_router
from admin.adapter.inbound.api.v1.piper_name_router import name_router
from ontology.adapter.inbound.api import vision_router, route_router
from rag.adapter.inbound.api import rag_router
from titanic.adapter.inbound.api import titanic_router

AsyncSessionDep = Annotated[AsyncSession, Depends(get_db)]
DatabaseHealthAdapterDep = Annotated[DatabaseHealthAdapter, Depends(get_db_health_adapter)]

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s:     %(message)s",
)
logger = logging.getLogger(__name__)


async def _init_friday13th_tables() -> None:
    engine = get_engine()
    if engine is None:
        logger.warning("DATABASE_URL 없음 — friday13th_users 테이블 생성을 건너뜁니다.")
        return
    async with engine.begin() as conn:
        await conn.run_sync(Friday13thBase.metadata.create_all)
    logger.info("Neon friday13th_users 테이블 준비 완료")


async def _init_titanic_tables() -> None:
    engine = get_engine()
    if engine is None:
        logger.warning("DATABASE_URL 없음 — titanic_person/booking 테이블 생성을 건너뜁니다.")
        return
    await create_titanic_tables()
    logger.info("Neon titanic_person / titanic_booking 테이블 준비 완료")


@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    configure_engine(settings.database_url)
    await _init_friday13th_tables()
    await _init_titanic_tables()
    try:
        yield
    finally:
        await dispose_engine()


app = FastAPI(title="titanic main Page", lifespan=lifespan, docs_url=None, redoc_url=None, openapi_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

_docs_security = HTTPBasic()


def _require_docs_auth(credentials: HTTPBasicCredentials = Depends(_docs_security)) -> None:
    settings = get_settings()
    if not settings.docs_username or not settings.docs_password:
        raise HTTPException(status_code=503, detail="문서 접근 인증이 설정되지 않았습니다.")
    valid_username = secrets.compare_digest(credentials.username, settings.docs_username)
    valid_password = secrets.compare_digest(credentials.password, settings.docs_password)
    if not (valid_username and valid_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증에 실패했습니다.",
            headers={"WWW-Authenticate": "Basic"},
        )


@app.get("/docs", include_in_schema=False)
def get_protected_docs(_: None = Depends(_require_docs_auth)) -> HTMLResponse:
    return get_swagger_ui_html(openapi_url="/openapi.json", title=f"{app.title} - Swagger UI")


@app.get("/redoc", include_in_schema=False)
def get_protected_redoc(_: None = Depends(_require_docs_auth)) -> HTMLResponse:
    return get_redoc_html(openapi_url="/openapi.json", title=f"{app.title} - ReDoc")


@app.get("/openapi.json", include_in_schema=False)
def get_protected_openapi(_: None = Depends(_require_docs_auth)) -> JSONResponse:
    return JSONResponse(app.openapi())

app.include_router(chat_router)
for friday13th_router in friday13th_v1_routers:
    app.include_router(friday13th_router)
for scout_router in scout_routers:
    app.include_router(scout_router)
app.include_router(community_router)
app.include_router(admin_router, dependencies=[Depends(RoleChecker(Role.ADMIN))])
app.include_router(name_router, prefix="/api/v1")
app.include_router(titanic_router)
app.include_router(vision_router)
app.include_router(route_router)
app.include_router(rag_router)

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8" />
<title>로그인</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f9fafb; display: flex; align-items: center; justify-content: center; min-height: 100vh; margin: 0; }
  .card { background: #fff; border: 1px solid #e5e7eb; border-radius: 12px; padding: 32px; width: 320px; box-shadow: 0 1px 3px rgba(0,0,0,.1); text-align: center; }
  h1 { font-size: 1.25rem; margin: 0 0 24px; color: #111827; }
  a.google-btn { display: flex; align-items: center; justify-content: center; gap: 8px; border: 1px solid #d1d5db; border-radius: 8px; padding: 10px 16px; text-decoration: none; color: #374151; font-size: .875rem; font-weight: 500; }
  a.google-btn:hover { background: #f9fafb; }
  a.naver-btn { display: flex; align-items: center; justify-content: center; gap: 8px; border: none; border-radius: 8px; padding: 10px 16px; text-decoration: none; color: #fff; background: #03c75a; font-size: .875rem; font-weight: 500; margin-top: 12px; }
  a.naver-btn:hover { background: #02b350; }
  .naver-mark { display: inline-flex; width: 16px; height: 16px; align-items: center; justify-content: center; font-size: 13px; font-weight: 900; line-height: 1; }
</style>
</head>
<body>
  <div class="card">
    <h1>로그인</h1>
    <a class="google-btn" href="/auth/google/login">
      <svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true">
        <path fill="#4285F4" d="M23.52 12.27c0-.85-.08-1.67-.22-2.45H12v4.64h6.47a5.53 5.53 0 0 1-2.4 3.63v3h3.88c2.27-2.09 3.57-5.17 3.57-8.82z"/>
        <path fill="#34A853" d="M12 24c3.24 0 5.95-1.07 7.94-2.91l-3.88-3a7.14 7.14 0 0 1-10.62-3.76H1.44v3.1A12 12 0 0 0 12 24z"/>
        <path fill="#FBBC05" d="M5.44 14.33a7.2 7.2 0 0 1 0-4.66v-3.1H1.44a12 12 0 0 0 0 10.86z"/>
        <path fill="#EA4335" d="M12 4.76c1.76 0 3.35.6 4.6 1.79l3.44-3.44C17.94 1.19 15.24 0 12 0A12 12 0 0 0 1.44 6.57l4 3.1A7.15 7.15 0 0 1 12 4.76z"/>
      </svg>
      구글로 로그인
    </a>
    <a class="naver-btn" href="https://anjgkwl.com/api/auth/naver/login">
      <span class="naver-mark" aria-hidden="true">N</span>
      네이버로 로그인
    </a>
  </div>
</body>
</html>"""


@app.get("/health/db")
async def read_db_health(
    db: AsyncSessionDep,
    adapter: DatabaseHealthAdapterDep,
):
    return await adapter.check_neon_now(db)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        app_dir=str(_ROOT),
    )
