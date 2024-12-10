from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr
from src.schemas.base import BaseSchema


class BaseUser(BaseSchema):
    username: str
    email: EmailStr


class ShowUser(BaseUser):
    id: UUID


class CreateUser(BaseUser):
    password: str


class UpdateUser(BaseUser):
    username: str
    email: EmailStr
    is_active: bool


class ParticularUpdateUser(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    is_active: bool | None = None
