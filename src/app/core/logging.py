from pathlib import Path
import sys

from loguru import logger

from app.core.config import get_settings

settings = get_settings()


def setup_logging(level: str = "INFO") -> None:
    logger.remove()  # Remove default logger

    log_format = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"

    # 콘솔 출력 추가
    logger.add(
        sys.stdout,
        level=level,
        format=log_format,
        colorize=True,
        enqueue=True,  # 비동기 로깅 지원
    )

    log_path = Path(settings.LOG_FILE_PATH)
    log_path.parent.mkdir(parents=True, exist_ok=True)  # 로그 디렉토리가 없으면 생성

    # 파일 출력 추가
    logger.add(
        settings.LOG_FILE_PATH,
        level=level,
        rotation=settings.LOG_ROTATION,
        retention=settings.LOG_RETENTION,
        format=log_format,
    )
