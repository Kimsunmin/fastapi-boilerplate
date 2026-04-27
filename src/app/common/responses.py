from typing import Literal, Generic, TypeVar
from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    """공통 API 응답 포맷"""

    status: Literal["success", "error"]
    code: str | None = None
    message: str
    data: T | None = None


def ok(data=None, message: str = "Success", code: str = "OK") -> dict:
    """성공 응답 생성"""
    return {
        "status": "success",
        "code": code,
        "message": message,
        "data": data,
    }
