from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.movies import (
    CreateMovieSchema,
    ShowMovieSchema,
    UpdateMovieSchema,
    PartialUpdateMovieSchema,
)
from src.services.crud.base import ModelManager
from src.models.movies import Movie


class TaskManager(
    ModelManager[
        Movie,
        ShowMovieSchema,
        CreateMovieSchema,
        UpdateMovieSchema,
        PartialUpdateMovieSchema,
    ]
):
    pass


crud_movies = TaskManager(Movie)


async def user_movies(
    user_id: UUID,
    session: AsyncSession,
    page_size: int,
    page_number: int,
) -> list[Movie]:
    page_from = page_size * (page_number - 1)
    movies = await session.scalars(
        select(Movie).where(Movie.user_id == user_id).offset(page_from).limit(page_size)
    )
    return list(movies)
