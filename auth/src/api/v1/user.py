from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.auth_utils import auth_utils
from src.db.session import db_session
from src.models import User
from src.schemas.user import (
    ShowUserSchema,
    CreateUserSchema,
    ParticularUpdateUserSchema,
    UpdateUserSchema,
)
from src.services.crud import user as crud_user
import logging


router = APIRouter()

logger = logging.getLogger(__name__)


@router.get(
    "/",
    response_model=list[ShowUserSchema],
    dependencies=[Depends(auth_utils.get_current_active_user)],
)
async def get_user(
    session: AsyncSession = Depends(db_session.get_session),
) -> [ShowUserSchema]:
    result = await crud_user.get_active_users(session)
    return result


@router.post("/", response_model=ShowUserSchema, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: CreateUserSchema,
    session: AsyncSession = Depends(db_session.get_session),
):
    return await crud_user.create_user(user, session)


@router.get(
    "/{user_id}",
    response_model=ShowUserSchema,
    dependencies=[Depends(auth_utils.get_current_active_user)],
)
async def get_user(
    user: ShowUserSchema = Depends(crud_user.get_active_user_by_uuid),
) -> ShowUserSchema:
    return user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(auth_utils.get_current_active_user)],
)
async def delete_user(
    user: User = Depends(crud_user.get_user_by_uuid),
    session: AsyncSession = Depends(db_session.get_session),
):
    await crud_user.delete_user(session, user)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowUserSchema,
    dependencies=[Depends(auth_utils.get_current_active_user)],
)
async def partial_update_user(
    user_schema: ParticularUpdateUserSchema,
    user: User = Depends(crud_user.get_active_user_by_uuid),
    session: AsyncSession = Depends(db_session.get_session),
):
    return await crud_user.update_user(
        session=session, user=user, user_schema=user_schema, particular=True
    )


@router.put(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowUserSchema,
    dependencies=[Depends(auth_utils.get_current_active_user)],
)
async def update_user(
    user_schema: UpdateUserSchema,
    user: User = Depends(crud_user.get_active_user_by_uuid),
    session: AsyncSession = Depends(db_session.get_session),
):
    return await crud_user.update_user(
        session=session,
        user=user,
        user_schema=user_schema,
    )
