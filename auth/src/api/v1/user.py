from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Response, status, Path, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.auth_utils import auth_utils
from src.db.session import db_session
from src.models import User
from src.schemas.user import (
    ShowUserSchema,
    CreateUserSchema,
    ParticularUpdateUserSchema,
    UpdateUserSchema,
    AddRoleToUserSchema,
    ShowUserWithRolesSchema,
)
from src.services.crud import user as crud_user
from src.services.crud import permissions as crud_permissions
from src.utils.check_permissions import check_permissions
import logging


router = APIRouter()

logger = logging.getLogger(__name__)


@router.get(
    "/",
    response_model=list[ShowUserSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(auth_utils.get_current_active_user)],
)
@check_permissions(["user"])
async def get_users(
    request: Request,
    session: AsyncSession = Depends(db_session.get_session),
) -> list[User]:
    return await crud_user.get_active_users(session)


@router.post(
    "/",
    response_model=ShowUserSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user: CreateUserSchema,
    session: AsyncSession = Depends(db_session.get_session),
) -> User:
    return await crud_user.create_user(user, session)


@router.get(
    "/{user_id}",
    response_model=ShowUserSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(auth_utils.get_current_active_user)],
)
async def get_user(
    user_id: Annotated[UUID, Path],
    session: AsyncSession = Depends(db_session.get_session),
) -> User:
    return await crud_user.get_user_by_uuid(session=session, user_id=user_id)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(auth_utils.get_current_active_user)],
)
async def delete_user(
    user_id: Annotated[UUID, Path],
    session: AsyncSession = Depends(db_session.get_session),
) -> Response:
    await crud_user.delete_user(session=session, user_id=user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowUserSchema,
    dependencies=[Depends(auth_utils.get_current_active_user)],
)
async def partial_update_user(
    user_schema: ParticularUpdateUserSchema,
    user_id: Annotated[UUID, Path],
    session: AsyncSession = Depends(db_session.get_session),
) -> User:
    return await crud_user.update_user(
        session=session, user_id=user_id, user_schema=user_schema, particular=True
    )


@router.put(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=ShowUserSchema,
    dependencies=[Depends(auth_utils.get_current_active_user)],
)
async def update_user(
    user_schema: UpdateUserSchema,
    user_id: Annotated[UUID, Path],
    session: AsyncSession = Depends(db_session.get_session),
) -> User:
    return await crud_user.update_user(
        session=session,
        user_id=user_id,
        user_schema=user_schema,
    )


@router.get(
    "/{user_id}/roles",
    response_model=ShowUserWithRolesSchema,
    dependencies=[Depends(auth_utils.get_current_active_user)],
)
async def add_role_to_user(
    user_id: Annotated[UUID, Path],
    session: AsyncSession = Depends(db_session.get_session),
) -> User:
    return await crud_user.get_user_with_roles(user_id=user_id, session=session)


@router.post(
    "/{user_id}/add_role",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(auth_utils.get_current_active_user)],
)
async def add_role_to_user(
    user_id: Annotated[UUID, Path],
    role_id: AddRoleToUserSchema,
    session: AsyncSession = Depends(db_session.get_session),
) -> Response:
    await crud_permissions.add_role_to_user(
        user_id=user_id, role_id=role_id, session=session
    )
    return Response(status_code=status.HTTP_200_OK)
