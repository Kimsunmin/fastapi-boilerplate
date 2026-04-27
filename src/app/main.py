from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import setup_logging
from app.core.middleware import log_requests, request_id_middleware
from app.api.route import api_router
from app.db.base import Base
from app.db.session import get_engine


def create_app() -> FastAPI:
    """FastAPI 애플리케이션 팩토리"""
    settings = get_settings()
    setup_logging(level=settings.LOG_LEVEL)

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        Base.metadata.create_all(bind=get_engine())
        logger.info(f"Settings loaded: {settings.model_dump_json(indent=2)}")
        yield

    app = FastAPI(
        title=settings.APP_NAME,
        lifespan=lifespan,
    )

    # 미들웨어 등록
    # 주의: FastAPI는 middleware("http")를 등록 역순으로 실행합니다.
    # log_requests에서 request.state.request_id를 사용하므로,
    # request_id_middleware를 먼저 등록해야 먼저 실행됩니다.
    app.middleware("http")(request_id_middleware)
    app.middleware("http")(log_requests)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 예외 핸들러 등록
    register_exception_handlers(app)

    # 라우터 등록
    app.include_router(api_router, prefix=settings.API_PREFIX)

    return app


# 기본 실행: uvicorn app.main:app --app-dir src --reload --no-access-log
app = create_app()
