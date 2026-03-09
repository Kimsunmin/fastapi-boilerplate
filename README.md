# FastAPI REST API Boilerplate

이 프로젝트는 **FastAPI 기반 REST API 서비스를 빠르게 시작하기 위한 보일러플레이트**입니다.
프로젝트의 목표는 다음과 같습니다.

* API 서버를 **일관된 구조로 빠르게 시작**
* 코드의 **책임 분리(Separation of Concerns)**
* 프로젝트가 커져도 **구조가 무너지지 않도록 설계**
* 새로운 개발자가 프로젝트를 봤을 때 **어디에 무엇을 작성해야 하는지 명확하게 이해**

이 문서는 **프로젝트 구조, 각 영역의 역할, 코드 작성 컨벤션**을 설명합니다.
이 문서와 프로젝트 구조만 보면 “어디에 어떤 코드를 작성해야 하는지” 바로 이해할 수 있도록 하는 것이 목표입니다.

---

# 1. 기술 스택

현재 프로젝트는 다음 라이브러리를 기반으로 합니다.

### Runtime dependencies

* fastapi
* uvicorn
* sqlalchemy
* alembic
* pydantic-settings
* httpx
* loguru

### Dev dependencies

* pytest
* ruff
* mypy
* httpx (테스트용)

---

# 2. 프로젝트 구조

```
src/
 └── app/
     ├── main.py
     ├── api/
     │   ├── router.py
     │   └── v1/
     │       ├── health.py
     │       └── users.py
     │
     ├── core/
     │   ├── config.py
     │   ├── logging.py
     │   └── exceptions.py
     │
     ├── dependencies/
     │   ├── auth.py
     │   ├── services.py
     │   └── pagination.py
     │
     ├── domain/
     │   └── users/
     │       ├── schemas.py
     │       ├── service.py
     │       └── repository.py
     │
     ├── db/
     │   ├── base.py
     │   ├── session.py
     │   └── models/
     │       └── user.py
     │
     ├── integrations/
     │   └── external_api.py
     │
     └── common/
         ├── responses.py
         └── pagination.py

tests/
```

---

# 3. 요청 처리 흐름

API 요청은 아래와 같은 흐름을 따릅니다.

```
Client Request
    ↓
api (router)
    ↓
dependencies
    ↓
domain/service
    ↓
domain/repository
    ↓
db
```

외부 시스템 호출이 필요한 경우:

```
service
  ↓
integrations
```

각 레이어는 **명확한 책임을 가지고 분리되어야 합니다.**

---

# 4. 각 영역의 역할

## main.py

애플리케이션의 **엔트리포인트**입니다.

여기서는 다음 작업만 수행합니다.

* FastAPI 앱 생성
* router 등록
* middleware 등록
* startup / shutdown 처리
* 예외 핸들러 등록

중요한 원칙:

main.py에는 **비즈니스 로직을 작성하지 않습니다.**

---

## api/

HTTP 요청을 처리하는 **API 계층**입니다.

여기서는 다음을 담당합니다.

* URL 경로 정의
* HTTP method 정의
* 요청 데이터 검증
* 서비스 호출
* 응답 반환

예시

```
GET /api/v1/users
POST /api/v1/users
```

router는 가능한 한 **얇게 유지해야 합니다.**

router에서 다음과 같은 코드는 작성하지 않습니다.

* DB 쿼리
* 복잡한 비즈니스 로직
* 외부 API 호출 로직

---

## core/

애플리케이션 전반에서 사용하는 **기반 구성 요소**입니다.

예:

* 환경 설정
* 로깅 설정
* 보안 관련 유틸
* 공통 예외 처리
* middleware

대표 파일

```
config.py
logging.py
exceptions.py
```

core는 **특정 도메인에 종속되지 않는 코드**만 포함해야 합니다.

---

## dependencies/

FastAPI의 `Depends()`로 **주입되는 구성 요소**를 모아두는 공간입니다.

예를 들면 다음과 같은 것들이 있습니다.

* 현재 사용자 조회
* 권한 검사
* pagination 파라미터
* 서비스 생성

예시

```python
def get_user_service(db: Session = Depends(get_db)):
    repo = UserRepository(db)
    return UserService(repo)
```

dependencies는 **비즈니스 로직을 수행하는 곳이 아닙니다.**

---

## domain/

프로젝트의 **핵심 비즈니스 로직**이 위치하는 영역입니다.

도메인 기준으로 디렉토리를 나눕니다.

예

```
domain/
 └── users/
```

각 도메인은 다음 파일로 구성됩니다.

```
schemas.py
service.py
repository.py
```

### schemas

입출력 데이터 모델

예:

* 요청 payload
* 응답 구조

### service

비즈니스 규칙을 담당합니다.

예:

* 이메일 중복 검사
* 상태 검증
* 정책 적용

### repository

데이터 접근 로직을 담당합니다.

예:

* DB 조회
* DB 저장

---

## db/

데이터베이스 관련 설정과 모델을 정의합니다.

예

```
base.py
session.py
models/
```

### base.py

ORM base 클래스 정의

### session.py

DB 연결 및 session 관리

### models/

SQLAlchemy 모델 정의

db 레이어는 **비즈니스 규칙을 포함하지 않습니다.**

---

## integrations/

외부 시스템과 연동하는 코드를 분리합니다.

예

* 외부 REST API
* OpenSearch
* Redis
* S3

service에서 외부 시스템을 호출할 경우
직접 구현하지 않고 integrations 레이어를 사용합니다.

---

## common/

프로젝트 전체에서 사용하는 공통 유틸리티를 둡니다.

예

* 공통 응답 포맷
* pagination 응답
* 공통 enum
* helper 함수

---

# 5. 코드 작성 컨벤션

## 1. Router는 얇게 유지한다

router는 다음 역할만 수행합니다.

* 요청 수신
* validation
* service 호출
* 응답 반환

예

```python
@router.post("")
def create_user(payload: UserCreate, service: UserService = Depends(get_user_service)):
    return service.create_user(payload)
```

---

## 2. 비즈니스 로직은 service에 작성

비즈니스 규칙은 반드시 service에 위치해야 합니다.

예

```
domain/users/service.py
```

---

## 3. DB 접근은 repository에서만 수행

service에서 직접 SQL을 작성하지 않습니다.

```
service → repository → db
```

---

## 4. 외부 API 호출은 integrations 사용

service에서 직접 httpx를 호출하지 않습니다.

```
service → integrations → external api
```

---

## 5. 환경 설정은 core/config에서 관리

`.env` 값을 직접 읽지 않습니다.

반드시 settings 객체를 사용합니다.

---

## 6. 도메인 단위로 구조를 확장

새로운 기능이 생기면 domain 기준으로 디렉토리를 추가합니다.

예

```
domain/orders
domain/products
domain/payments
```

---

# 6. API 버전 관리

API는 버전 기준으로 관리합니다.

```
api/v1/
api/v2/
```

main에서 prefix를 설정합니다.

```
/api/v1
```

---

# 7. 테스트 구조

테스트 코드는 `tests` 디렉토리에 작성합니다.

예

```
tests/
 ├── api/
 ├── domain/
 └── integrations/
```

---

# 8. 실행 방법


## 개발 서버 실행

아래 명령어로 FastAPI 개발 서버를 실행할 수 있습니다.

```
uvicorn app.main:app --app-dir src --reload --no-access-log
```

- `--app-dir src`: src 폴더를 파이썬 모듈 경로로 인식시킴
- `--reload`: 코드 변경 시 자동으로 서버 재시작
- `--no-access-log`: uvicorn 기본 access log 비활성화 (커스텀 로그만 사용)

실행 후 http://localhost:8000/docs 에서 API 문서를 확인할 수 있습니다.

---

# 9. 프로젝트 확장 방향

프로젝트가 커질 경우 다음과 같은 컴포넌트가 추가될 수 있습니다.

* Redis 캐시
* 메시지 큐
* 검색 엔진
* background worker
* 인증 시스템

이러한 컴포넌트는 integrations 레이어를 통해 연결합니다.

---

# 10. 핵심 원칙

이 프로젝트는 다음 원칙을 기반으로 합니다.

1. 책임 분리
2. 비즈니스 로직 중심 구조
3. 확장 가능한 디렉토리 구조
4. 일관된 코드 작성 방식

---

이 문서와 프로젝트 구조를 기준으로
새로운 기능을 추가할 때는 다음 순서를 따르면 됩니다.

1. domain에 기능 추가
2. service 작성
3. repository 작성
4. api router 작성
5. dependencies 연결

이 과정을 따르면 프로젝트 구조를 유지하면서 기능을 확장할 수 있습니다.
