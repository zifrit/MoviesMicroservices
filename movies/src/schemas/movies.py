from uuid import UUID

from src.schemas.base import BaseSchema


class MovieSchema(BaseSchema):
    name: str
    description: str


class CreateMovieSchema(MovieSchema):
    pass


class CreateMovieWithUserIDSchema(MovieSchema):
    user_id: UUID


class ShowMovieSchema(MovieSchema):
    id: UUID


class UpdateMovieSchema(MovieSchema):
    pass


class PartialUpdateMovieSchema(MovieSchema):
    name: str | None
    description: str | None
