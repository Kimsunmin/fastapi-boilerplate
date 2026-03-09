from fastapi import FastAPI

from app.core.config import get_settings
from app.core.logging import setup_logging
from app.core.middleware import log_requests
from app.api.route import api_router

# 설정 객체 가져오기
settings = get_settings()

# 로깅 설정
setup_logging(level=settings.LOG_LEVEL)

# FastAPI 애플리케이션 생성
# 기본 실행: uvicorn app.main:app --app-dir src --reload --no-access-log
app = FastAPI(
    title=settings.APP_NAME,
)

# 미들웨어 등록
app.middleware("http")(log_requests)  # 요청과 응답을 로깅하는 미들웨어 등록

# 라우터 등록
app.include_router(api_router, prefix=settings.API_PREFIX)