# FastAPI REST API Boilerplate

FastAPI 기반 REST API 서비스를 빠르게 시작하기 위한 보일러플레이트입니다.

## 특징

- 일관된 프로젝트 구조
- 레이어 분리 (API → Service → Repository → DB)
- 환경 설정 관리 (pydantic-settings)
- 구조화된 로깅 (loguru)
- 요청 ID 추적 및 자동 로깅
- 전역 예외 처리
- Docker 지원

## 기술 스택

| 분류 | 라이브러리 |
|------|-----------|
| Runtime | FastAPI, Uvicorn, SQLAlchemy, Alembic, pydantic-settings, httpx, loguru |
| Dev | pytest, ruff, mypy |

## 프로젝트 구조

```
src/app/
 ├── main.py          # 엔트리포인트
 ├── api/             # HTTP 요청 처리 (router)
 ├── core/            # 설정, 예외, 로깅, 미들웨어
 ├── dependencies/    # FastAPI Depends() 주입
 ├── domain/          # 비즈니스 로직
 ├── db/              # DB 설정 및 모델
 ├── integrations/    # 외부 시스템 연동
 └── common/          # 공통 유틸리티
```

> 자세한 구조와 규칙은 `PROJECT_SPEC.md`를 참고하세요.

## 실행 방법

### 로컬 개발

```bash
# 가상환경 활성화 (uv 사용 권장)
uv sync

# 개발 서버 실행
uvicorn app.main:app --app-dir src --reload --no-access-log
```

- `--app-dir src`: src 폴더를 파이썬 모듈 경로로 인식
- `--reload`: 코드 변경 시 자동 재시작
- `--no-access-log`: uvicorn 기본 access log 비활성화

API 문서: http://localhost:8000/docs

### Docker

```bash
# .env 파일 복사 후 수정
cp .env.example .env

# 빌드 및 실행
docker-compose up --build -d
```

## 환경 설정

`.env.example`을 복사하여 `.env` 파일을 만들고 필요한 값을 설정하세요.

| 변수 | 기본값 | 설명 |
|------|--------|------|
| `ENV` | `local` | 실행 환경 |
| `APP_PORT` | `8000` | 서버 포트 |
| `LOG_LEVEL` | `INFO` | 로그 레벨 |
| `DB_URL` | `sqlite:///./db.sqlite3` | DB 연결 URL |

## API 엔드포인트

| Method | Path | 설명 |
|--------|------|------|
| GET | `/api/v1/health` | 서버 상태 확인 |

## 라이선스

MIT
