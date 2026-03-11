# =============================================================================
# Stage 1: Builder - 의존성 설치
# =============================================================================
FROM ghcr.io/astral-sh/uv:python3.11-bookworm-slim AS builder

WORKDIR /app

# 의존성 파일만 먼저 복사 (캐시 활용)
COPY pyproject.toml uv.lock ./

# 가상환경 생성 및 의존성 설치 (dev 제외)
RUN uv sync --frozen --no-dev

# =============================================================================
# Stage 2: Runtime - 실행 환경
# =============================================================================
FROM python:3.11-slim-bookworm AS runtime

WORKDIR /app

# 보안: non-root 사용자 생성
RUN groupadd --gid 1001 appgroup && \
    useradd --uid 1001 --gid appgroup --no-create-home appuser

# 빌더 스테이지에서 가상환경만 복사
COPY --from=builder /app/.venv /app/.venv

# 소스코드 복사
COPY src/ ./src/

# 로그 디렉토리 생성 및 권한 설정
RUN mkdir -p logs && chown -R appuser:appgroup /app

# 환경변수 설정
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    ENV=production

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/v1/health')" || exit 1

CMD ["uvicorn", "app.main:app", "--app-dir", "src", "--host", "0.0.0.0", "--port", "8000", "--no-access-log"]
