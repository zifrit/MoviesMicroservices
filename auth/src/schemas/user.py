from uuid import UUID

from pydantic import EmailStr
from src.schemas.base import BaseSchema


class BaseUserSchema(BaseSchema):
    username: str
    email: EmailStr


class ShowUserSchema(BaseUserSchema):
    id: UUID


class CreateUserSchema(BaseUserSchema):
    password: str


class UpdateUserSchema(BaseUserSchema):
    username: str
    email: EmailStr
    is_active: bool


class ParticularUpdateUserSchema(BaseSchema):
    username: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None


class UserLoginSchema(BaseSchema):
    username: str
    password: str
