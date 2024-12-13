from uuid import UUID

from src.schemas.base import BaseSchema


class UserSchema(BaseSchema):
    username: str
    user_id: UUID
