from uuid import UUID

from src.schemas.base import BaseSchema


class MovieSchema(BaseSchema):
    name: str
    description: str


class CreateMovieSchema(MovieSchema):
    pass


class ShowMovieSchema(MovieSchema):
    id: UUID


class UpdateMovieSchema(MovieSchema):
    pass


class PartialUpdateMovieSchema(MovieSchema):
    name: str | None
    description: str | None
