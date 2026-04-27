# Project Specification

> 이 문서는 **LLM/코딩 에이전트가 이 프로젝트의 구조와 규칙을 일관되게 따륏도록 하기 위한 기술 명세**입니다.
> 프로젝트를 확장하거나 수정할 때 이 문서를 컨텍스트로 제공하세요.

---

## 1. 프로젝트 개요

| 항목 | 내용 |
|------|------|
| **프로젝트명** | fastapi-boilerplate |
| **버전** | 0.1.0 |
| **프레임워크** | FastAPI |
| **Python** | >= 3.11 |
| **패키지 관리** | uv |

---

## 2. 아키텍처 원칙

1. **책임 분리 (Separation of Concerns)**
2. **비즈니스 로직 중심 구조**
3. **확장 가능한 디렉토리 구조**
4. **일관된 코드 작성 방식**

---

## 3. 레이어 구조 및 규칙

### 3.1 요청 처리 흐름

```
Client Request
    ↓
api (router)        ← URL 정의, validation, 응답 반환만
    ↓
dependencies        ← FastAPI Depends() 주입 (service 생성, auth 등)
    ↓
domain/service      ← 비즈니스 규칙 (중복 검사, 상태 검증, 정책)
    ↓
domain/repository   ← DB 접근 (조회, 저장)
    ↓
db                  ← SQLAlchemy 모델, session
```

외부 시스템 호출 시:

```
service
  ↓
integrations        ← 외부 API, Redis, S3 등
```

### 3.2 각 레이어의 절대 금지 사항

| 레이어 | 하면 안 되는 것 |
|--------|----------------|
| `api/` | DB 쿼리, 복잡한 비즈니스 로직, 외부 API 호출 |
| `domain/service/` | SQL 직접 작성, httpx 직접 호출 |
| `domain/repository/` | 비즈니스 규칙 포함 |
| `db/` | 비즈니스 규칙 포함 |
| `core/` | 특정 도메인에 종속된 코드 |

---

## 4. 디렉토리 구조

```
src/app/
 ├── main.py              # 엔트리포인트. 앱 생성, router/middleware/예외핸들러 등록만
 ├── api/
 │   ├── route.py         # APIRouter 집합. 모든 v1 router를 include
 │   └── v1/
 │       └── *.py         # 엔드포인트 정의. 얇게 유지
 ├── core/
 │   ├── config.py        # pydantic-settings 기반 환경 설정
 │   ├── exceptions.py    # AppException 기반 예외 클래스 + 핸들러 등록 함수
 │   ├── logging.py       # loguru 설정
 │   └── middleware.py    # 커스텀 미들웨어 (request_id, logging 등)
 ├── dependencies/
 │   └── *.py             # FastAPI Depends()로 주입되는 함수들
 ├── domain/
 │   └── {도메인명}/
 │       ├── schemas.py   # Pydantic 모델 (요청/응답)
 │       ├── service.py   # 비즈니스 로직
 │       └── repository.py # DB 접근 로직
 ├── db/
 │   ├── base.py          # SQLAlchemy declarative base
 │   ├── session.py       # DB 연결, session 관리
 │   └── models/
 │       └── *.py         # SQLAlchemy 모델
 ├── integrations/
 │   └── *.py             # 외부 시스템 연동
 └── common/
     └── *.py             # 공통 유틸 (응답 포맷, pagination, enum 등)

tests/
 ├── api/
 ├── domain/
 └── integrations/
```

---

## 5. 코드 작성 규칙

### 5.1 Router는 얇게 유지

```python
# ✅ 올바른 예
@router.post("")
def create_user(payload: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create_user(payload)

# ❌ 잘못된 예: DB 쿼리, 비즈니스 로직, 외부 API 호출 금지
```

### 5.2 비즈니스 로직은 service에

- 이메일 중복 검사
- 상태 검증
- 정책 적용

### 5.3 DB 접근은 repository에서만

```
service → repository → db
```

### 5.4 외부 API 호출은 integrations 사용

```
service → integrations → external api
```

### 5.5 환경 설정은 core/config에서만

`.env` 값을 직접 읽지 않고 반드시 `get_settings()`를 사용합니다.

### 5.6 도메인 단위로 확장

새 기능 추가 시:

```
domain/orders/
domain/products/
domain/payments/
```

각 도메인은 `schemas.py`, `service.py`, `repository.py`를 포함합니다.

---

## 6. 예외 처리 규칙

- 모든 커스텀 예외는 `AppException`을 상속합니다.
- 예외 핸들러 등록은 `core/exceptions.py`의 `register_exception_handlers(app)`를 사용합니다.
- `main.py`에서 직접 `@app.exception_handler`를 작성하지 않습니다.

### 6.1 예외 클래스

| 클래스 | 상태 코드 | 용도 |
|--------|----------|------|
| `BadRequestException` | 400 | 잘못된 요청 |
| `UnauthorizedException` | 401 | 인증 필요 |
| `ForbiddenException` | 403 | 권한 없음 |
| `NotFoundException` | 404 | 대상 없음 |
| `ConflictException` | 409 | 중복/충돌 |

---

## 7. 미들웨어 규칙

- `middleware("http")`는 **등록 역순**으로 실행됩니다.
- `request_id_middleware`가 먼저 실행되어야 `log_requests`가 `request.state.request_id`를 사용할 수 있습니다.
- 따라서 등록 순서: `request_id_middleware` → `log_requests`

---

## 8. API 버전 관리

- 버전 기준 디렉토리: `api/v1/`, `api/v2/`
- prefix: `/api/v1`
- `api/route.py`에서 모든 버전 router를 include

---

## 9. 환경 설정 변수

| 변수명 | 기본값 | 설명 |
|--------|--------|------|
| `ENV` | `local` | 실행 환경 |
| `APP_NAME` | `fastapi-boilerplate` | 앱 이름 |
| `APP_PORT` | `8000` | 서버 포트 |
| `API_PREFIX` | `/api/v1` | API prefix |
| `DB_URL` | `sqlite:///./db.sqlite3` | DB 연결 URL |
| `LOG_LEVEL` | `INFO` | 로그 레벨 |
| `LOG_FILE_PATH` | `logs/app.log` | 로그 파일 경로 |
| `LOG_ROTATION` | `1 day` | 로그 순환 주기 |
| `LOG_RETENTION` | `7 days` | 로그 보관 기간 |
| `DOCKER_IMAGE_NAME` | `fastapi-boilerplate` | Docker 이미지명 |
| `DOCKER_IMAGE_TAG` | `latest` | Docker 이미지 태그 |
| `DOCKER_CONTAINER_NAME` | `fastapi-boilerplate` | Docker 컨테이너명 |

---

## 10. 기능 확장 순서

새로운 기능을 추가할 때 다음 순서를 따릅니다:

1. `domain/{도메인}/`에 디렉토리 생성 → `schemas.py`, `service.py`, `repository.py` 작성
2. `dependencies/`에 service 주입 함수 작성
3. `api/v1/`에 router 작성
4. `api/route.py`에 router include
5. 필요시 `db/models/`에 SQLAlchemy 모델 추가
6. 테스트 코드 작성 (`tests/`)

---

## 11. 의존성

### Runtime
- fastapi >= 0.135.1
- uvicorn >= 0.41.0
- sqlalchemy >= 2.0.48
- alembic >= 1.18.4
- pydantic-settings >= 2.13.1
- httpx >= 0.28.1
- loguru >= 0.7.3

### Dev
- pytest >= 9.0.2
- ruff >= 0.15.5
- mypy >= 1.19.1
