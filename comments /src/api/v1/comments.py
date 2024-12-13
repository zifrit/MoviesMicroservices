from uuid import UUID

from src.models import Comments
from src.schemas.comments import (
    CreateCommentsSchema,
    CreateCommentsWithUserIDSchema,
    UpdateCommentsSchema,
    PartialUpdateCommentsSchema,
    ShowCommentsSchema,
)
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Response, status, Query, Request

from src.schemas.users import UserSchema
from src.services.crud.comments import crud_comments, user_comments
from src.db.session import db_session
from src.utils.auth_utils import auth_utils
from src.utils.check_permissions import check_permissions


router = APIRouter()


@router.post(
    "/",
    response_model=ShowCommentsSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(auth_utils.get_current_user)],
)
@check_permissions(["user"])
async def create_comments(
    request: Request,
    comments_schema: CreateCommentsSchema,
    user: UserSchema = Depends(auth_utils.get_current_user),
    session: AsyncSession = Depends(db_session.get_session),
) -> ShowCommentsSchema:
    comments_schema_with_user_id = CreateCommentsWithUserIDSchema(
        **comments_schema.model_dump(), user_id=user.user_id
    )
    return await crud_comments.create(
        session=session, obj_schema=comments_schema_with_user_id
    )


@router.get(
    "/",
    response_model=list[ShowCommentsSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(auth_utils.get_current_user)],
)
@check_permissions(["user"])
async def get_comments(
    request: Request,
    page_size: int = Query(
        ge=1, le=100, description="Количество элементов на странице", default=1
    ),
    page_number: int = Query(ge=1, description="Номер страницы", default=1),
    session: AsyncSession = Depends(db_session.get_session),
) -> list[ShowCommentsSchema]:
    return await crud_comments.get(
        session=session,
        page_size=page_size,
        page_number=page_number,
    )


@router.get(
    "/user/user_id",
    response_model=list[ShowCommentsSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(auth_utils.get_current_user)],
)
@check_permissions(["user"])
async def get_user_comments(
    request: Request,
    user_id: UUID,
    session: AsyncSession = Depends(db_session.get_session),
    page_size: int = Query(
        ge=1, le=100, description="Количество элементов на странице", default=1
    ),
    page_number: int = Query(ge=1, description="Номер страницы", default=1),
) -> list[Comments]:
    return await user_comments(
        session=session,
        user_id=user_id,
        page_size=page_size,
        page_number=page_number,
    )


@router.get(
    "/{movie_id}",
    response_model=ShowCommentsSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(auth_utils.get_current_user)],
)
@check_permissions(["user"])
async def get_comment(
    request: Request,
    comment_id: UUID,
    session: AsyncSession = Depends(db_session.get_session),
) -> ShowCommentsSchema:
    return await crud_comments.get_by_id(session=session, id_=comment_id)


@router.put(
    "/{movie_id}",
    response_model=ShowCommentsSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(auth_utils.get_current_user)],
)
@check_permissions(["user"])
async def update_comments(
    request: Request,
    movie_id: UUID,
    comments_schema: UpdateCommentsSchema,
    session: AsyncSession = Depends(db_session.get_session),
) -> ShowCommentsSchema:
    return await crud_comments.update(
        session=session,
        obj_schema=comments_schema,
        id_=movie_id,
    )


@router.patch(
    "/{movie_id}",
    response_model=ShowCommentsSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(auth_utils.get_current_user)],
)
@check_permissions(["user"])
async def particular_update_comments(
    request: Request,
    movie_id: UUID,
    comments_schema: PartialUpdateCommentsSchema,
    session: AsyncSession = Depends(db_session.get_session),
) -> ShowCommentsSchema:
    return await crud_comments.update(
        session=session,
        obj_schema=comments_schema,
        id_=movie_id,
        particular=True,
    )


@router.delete(
    "/{movie_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(auth_utils.get_current_user)],
)
@check_permissions(["user"])
async def delete_comments(
    request: Request,
    comments_id: UUID,
    session: AsyncSession = Depends(db_session.get_session),
) -> Response:
    await crud_comments.delete(session=session, id_=comments_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
