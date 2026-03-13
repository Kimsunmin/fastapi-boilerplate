from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.core.middleware import log_requests, request_id_middleware
from app.api.route import api_router

# 설정 객체 가져오기
settings = get_settings()

# 로깅 설정
setup_logging(level=settings.LOG_LEVEL)

# lifespan 애플리케이션 생성
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 애플리케이션이 시작될 때 실행할 코드
    logger.info(f"Settings loaded: {settings.model_dump_json(indent=2)}")
    yield
    # 애플리케이션이 종료될 때 실행할 코드

# FastAPI 애플리케이션 생성
# 기본 실행: uvicorn app.main:app --app-dir src --reload --no-access-log
app = FastAPI(
    title=settings.APP_NAME,
    lifespan=lifespan,
)

# 미들웨어 등록
app.middleware("http")(request_id_middleware)  # 요청 ID를 생성하고 응답 헤더에 추가하는 미들웨어 등록
app.middleware("http")(log_requests)  # 요청과 응답을 로깅하는 미들웨어 등록

# 라우터 등록
app.include_router(api_router, prefix=settings.API_PREFIX)