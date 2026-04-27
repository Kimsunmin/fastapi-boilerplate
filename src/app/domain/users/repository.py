from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.models.user import User
from app.domain.users.schemas import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.db.execute(stmt).scalar_one_or_none()

    def get_all(self) -> list[User]:
        stmt = select(User)
        return list(self.db.execute(stmt).scalars().all())

    def create(self, data: UserCreate) -> User:
        user = User(email=str(data.email), name=data.name)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User, data: UserUpdate) -> User:
        if data.email is not None:
            user.email = str(data.email)
        if data.name is not None:
            user.name = data.name
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()
