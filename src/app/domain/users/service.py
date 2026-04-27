from app.core.exceptions import ConflictException, NotFoundException
from app.domain.users.schemas import UserCreate, UserUpdate, UserResponse
from app.domain.users.repository import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_user(self, user_id: int) -> UserResponse:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundException(message="사용자를 찾을 수 없습니다.")
        return UserResponse.model_validate(user)

    def list_users(self) -> list[UserResponse]:
        users = self.repository.get_all()
        return [UserResponse.model_validate(u) for u in users]

    def create_user(self, data: UserCreate) -> UserResponse:
        existing = self.repository.get_by_email(str(data.email))
        if existing:
            raise ConflictException(message="이미 등록된 이메일입니다.")
        user = self.repository.create(data)
        return UserResponse.model_validate(user)

    def update_user(self, user_id: int, data: UserUpdate) -> UserResponse:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundException(message="사용자를 찾을 수 없습니다.")

        if data.email is not None:
            existing = self.repository.get_by_email(str(data.email))
            if existing and existing.id != user_id:
                raise ConflictException(message="이미 등록된 이메일입니다.")

        updated = self.repository.update(user, data)
        return UserResponse.model_validate(updated)

    def delete_user(self, user_id: int) -> None:
        user = self.repository.get_by_id(user_id)
        if not user:
            raise NotFoundException(message="사용자를 찾을 수 없습니다.")
        self.repository.delete(user)
