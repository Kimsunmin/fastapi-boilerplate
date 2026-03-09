from fastapi import status


class AppException(Exception):
    """전역 기본 예외 클래스"""

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        data: dict | None = None,
    ):
        self.code = code
        self.message = message
        self.status_code = status_code
        self.data = data
        super().__init__(message)


class BadRequestException(AppException):
    def __init__(self, message: str = "잘못된 요청입니다.", code: str = "BAD_REQUEST"):
        super().__init__(
            code=code,
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class UnauthorizedException(AppException):
    def __init__(self, message: str = "인증이 필요합니다.", code: str = "UNAUTHORIZED"):
        super().__init__(
            code=code,
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class ForbiddenException(AppException):
    def __init__(self, message: str = "권한이 없습니다.", code: str = "FORBIDDEN"):
        super().__init__(
            code=code,
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
        )


class NotFoundException(AppException):
    def __init__(
        self, message: str = "대상을 찾을 수 없습니다.", code: str = "NOT_FOUND"
    ):
        super().__init__(
            code=code,
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
        )


class ConflictException(AppException):
    def __init__(self, message: str = "이미 존재합니다.", code: str = "CONFLICT"):
        super().__init__(
            code=code,
            message=message,
            status_code=status.HTTP_409_CONFLICT,
        )
