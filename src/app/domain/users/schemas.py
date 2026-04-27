from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    name: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    name: str | None = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
