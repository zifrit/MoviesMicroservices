from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.comments import (
    CreateCommentsSchema,
    ShowCommentsSchema,
    UpdateCommentsSchema,
    PartialUpdateCommentsSchema,
)
from src.services.crud.base import ModelManager
from src.models.movies import Comments


class CommentsManager(
    ModelManager[
        Comments,
        ShowCommentsSchema,
        CreateCommentsSchema,
        UpdateCommentsSchema,
        PartialUpdateCommentsSchema,
    ]
):
    pass


crud_comments = CommentsManager(Comments)


async def user_comments(
    user_id: UUID,
    session: AsyncSession,
    page_size: int,
    page_number: int,
) -> list[Comments]:
    page_from = page_size * (page_number - 1)
    comments = await session.scalars(
        select(Comments)
        .where(Comments.user_id == user_id)
        .offset(page_from)
        .limit(page_size)
    )
    return list(comments)
