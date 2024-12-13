from uuid import UUID

from src.models import Movie
from src.schemas.movies import (
    CreateMovieSchema,
    CreateMovieWithUserIDSchema,
    UpdateMovieSchema,
    PartialUpdateMovieSchema,
    ShowMovieSchema,
)
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Response, status, Query, Request

from src.schemas.users import UserSchema
from src.services.crud.movies import crud_movies, user_movies
from src.db.session import db_session
from src.utils.auth_utils import auth_utils
from src.utils.check_permissions import check_permissions


router = APIRouter()


@router.post(
    "/",
    response_model=ShowMovieSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(auth_utils.get_current_user)],
)
@check_permissions(["user"])
async def create_movie(
    request: Request,
    movie_schema: CreateMovieSchema,
    user: UserSchema = Depends(auth_utils.get_current_user),
    session: AsyncSession = Depends(db_session.get_session),
) -> ShowMovieSchema:
    movie_schema_with_user_id = CreateMovieWithUserIDSchema(
        **movie_schema.model_dump(), user_id=user.user_id
    )
    return await crud_movies.create(
        session=session, obj_schema=movie_schema_with_user_id
    )


@router.get(
    "/",
    response_model=list[ShowMovieSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(auth_utils.get_current_user)],
)
@check_permissions(["user"])
async def get_movies(
    request: Request,
    page_size: int = Query(
        ge=1, le=100, description="Количество элементов на странице", default=1
    ),
    page_number: int = Query(ge=1, description="Номер страницы", default=1),
    session: AsyncSession = Depends(db_session.get_session),
) -> list[ShowMovieSchema]:
    return await crud_movies.get(
        session=session,
        page_size=page_size,
        page_number=page_number,
    )


@router.get(
    "/user/user_id",
    response_model=list[ShowMovieSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(auth_utils.get_current_user)],
)
@check_permissions(["user"])
async def get_user_movies(
    request: Request,
    user_id: UUID,
    session: AsyncSession = Depends(db_session.get_session),
    page_size: int = Query(
        ge=1, le=100, description="Количество элементов на странице", default=1
    ),
    page_number: int = Query(ge=1, description="Номер страницы", default=1),
) -> list[Movie]:
    return await user_movies(
        session=session,
        user_id=user_id,
        page_size=page_size,
        page_number=page_number,
    )


@router.get(
    "/{movie_id}",
    response_model=ShowMovieSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(auth_utils.get_current_user)],
)
@check_permissions(["user"])
async def get_movie(
    request: Request,
    movie_id: UUID,
    session: AsyncSession = Depends(db_session.get_session),
) -> ShowMovieSchema:
    return await crud_movies.get_by_id(session=session, id_=movie_id)


@router.put(
    "/{movie_id}",
    response_model=ShowMovieSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(auth_utils.get_current_user)],
)
@check_permissions(["user"])
async def update_movie(
    request: Request,
    movie_id: UUID,
    movie_schema: UpdateMovieSchema,
    session: AsyncSession = Depends(db_session.get_session),
) -> ShowMovieSchema:
    return await crud_movies.update(
        session=session,
        obj_schema=movie_schema,
        id_=movie_id,
    )


@router.patch(
    "/{movie_id}",
    response_model=ShowMovieSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(auth_utils.get_current_user)],
)
@check_permissions(["user"])
async def particular_update_movie(
    request: Request,
    movie_id: UUID,
    movie_schema: PartialUpdateMovieSchema,
    session: AsyncSession = Depends(db_session.get_session),
) -> ShowMovieSchema:
    return await crud_movies.update(
        session=session,
        obj_schema=movie_schema,
        id_=movie_id,
        particular=True,
    )


@router.delete(
    "/{movie_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(auth_utils.get_current_user)],
)
@check_permissions(["user"])
async def delete_movie(
    request: Request,
    movie_id: UUID,
    session: AsyncSession = Depends(db_session.get_session),
) -> Response:
    await crud_movies.delete(session=session, id_=movie_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
