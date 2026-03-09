from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "local"

    APP_NAME: str = "fastapi-boilerplate"
    API_PREFIX: str = "/api/v1"

    DB_URL: str = "sqlite:///./db.sqlite3"
    
    # 로깅 설정
    LOG_LEVEL: str = "INFO"
    LOG_FILE_PATH: str = "logs/app.log"
    LOG_ROTATION: str = "1 day"
    LOG_RETENTION: str = "7 days"

    # env 파일 읽어오기
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# 캐싱된 설정 객체 반환
@lru_cache
def get_settings() -> Settings:
    return Settings()