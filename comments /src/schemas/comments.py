from uuid import UUID

from src.schemas.base import BaseSchema


class CommentsSchema(BaseSchema):
    text: str
    object_id: UUID


class CreateCommentsSchema(CommentsSchema):
    pass


class CreateCommentsWithUserIDSchema(CommentsSchema):
    user_id: UUID


class ShowCommentsSchema(CommentsSchema):
    id: UUID
    user_id: UUID


class UpdateCommentsSchema(CommentsSchema):
    pass


class PartialUpdateCommentsSchema(CommentsSchema):
    text: str | None = None
    object_id: str | None = None
