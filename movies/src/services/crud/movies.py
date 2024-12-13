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


crud_task = TaskManager(Movie)


async def get_user_movies(
    user_id: int,
) -> list[Movie]:
    pass
