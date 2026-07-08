import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

_BACKEND_ROOT = Path(__file__).resolve().parent.parent
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import get_settings
from core.matrix.chat_router import router as chat_router
from scout.adapter.inbound.api import scout_routers
from friday13th.adapter.inbound.api.v1 import friday13th_v1_routers
from friday13th.adapter.outbound.orm.user_model import Base as Friday13thBase
from core.database import (
    configure_engine,
    create_titanic_tables,
    dispose_engine,
    get_engine,
)
from core.deps import (
    AsyncSessionDep,
    DatabaseHealthAdapterDep,
    DoroDirectorDep,
)
from titanic.adapter.inbound.api import titanic_router

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


app = FastAPI(title="titanic main Page", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
for friday13th_router in friday13th_v1_routers:
    app.include_router(friday13th_router)
for scout_router in scout_routers:
    app.include_router(scout_router)
app.include_router(titanic_router)


@app.get("/")
def read_root():
    return {"message": "FAST API 메인 페이지 ", "docs": "/docs"}


@app.get("/health/db")
async def read_db_health(
    db: AsyncSessionDep,
    adapter: DatabaseHealthAdapterDep,
):
    return await adapter.check_neon_now(db)


@app.get("/doro/data")
def read_doro_data(doro: DoroDirectorDep):
    df = doro.get_data()
    return df.to_dict(orient="records")





if __name__ == "__main__":
    import uvicorn

    _APPS_DIR = Path(__file__).resolve().parent
    # app_dir 필수: backend/main.py(구 엔트리)와 이름 충돌 방지
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        app_dir=str(_APPS_DIR),
    )
