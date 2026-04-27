from fastapi import APIRouter, Depends, status

from app.common.responses import ok
from app.domain.users.schemas import UserCreate, UserUpdate, UserResponse
from app.domain.users.service import UserService
from app.dependencies.services import get_user_service


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("")
def list_users(service: UserService = Depends(get_user_service)):
    """사용자 목록 조회"""
    users = service.list_users()
    return ok(data=users)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(data: UserCreate, service: UserService = Depends(get_user_service)):
    """사용자 생성"""
    user = service.create_user(data)
    return ok(data=user, message="사용자가 생성되었습니다.", code="CREATED")


@router.get("/{user_id}")
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    """사용자 상세 조회"""
    user = service.get_user(user_id)
    return ok(data=user)


@router.patch("/{user_id}")
def update_user(user_id: int, data: UserUpdate, service: UserService = Depends(get_user_service)):
    """사용자 수정"""
    user = service.update_user(user_id, data)
    return ok(data=user, message="사용자가 수정되었습니다.")


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, service: UserService = Depends(get_user_service)):
    """사용자 삭제"""
    service.delete_user(user_id)
