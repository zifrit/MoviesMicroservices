from datetime import datetime, timezone
from typing import Annotated
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import load_only, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status, Path, Depends

from src.db.session import db_session
from src.models.user import User
from src.models.permissions import Roles

from src.schemas.user import (
    CreateUserSchema,
    UpdateUserSchema,
    ParticularUpdateUserSchema,
)
from src.utils import auth_utils
from src.utils.raising_http_excp import RaiseHttpException


async def create_user(
    user: CreateUserSchema,
    session: AsyncSession,
) -> User:
    new_user = User(
        username=user.username,
        password=auth_utils.auth_utils.hash_password(user.password),
        email=user.email,
    )
    try:
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
    except IntegrityError as e:
        await session.rollback()
        if "email" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )
        elif "username" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username already exists",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate entry for unique field",
            )
    return new_user


async def get_active_user_by_uuid(
    user_id: Annotated[UUID, Path],
    session: AsyncSession = Depends(db_session.get_session),
) -> User:
    user = await session.scalar(
        select(User).where(User.id == user_id, User.is_active == True)
    )
    return user if user else RaiseHttpException.check_is_exist(user)


async def get_user_by_uuid(
    user_id: UUID,
    session: AsyncSession,
) -> User:
    user = await session.scalar(select(User).where(User.id == user_id))
    return user if user else RaiseHttpException.check_is_exist(user)


async def get_active_user_by_username_with_roles(
    username: str,
    session: AsyncSession,
) -> User:
    user = await session.scalar(
        select(User)
        .options(
            selectinload(User.roles).load_only(
                Roles.id,
                Roles.name,
            ),
        )
        .where(
            User.username == username, User.deleted_at.is_(None), User.is_active == True
        )
    )
    return user if user else RaiseHttpException.check_is_exist(user)


async def get_active_users(session: AsyncSession) -> list[User]:
    users = await session.scalars(
        select(User).where(User.is_active == True, User.deleted_at.is_(None))
    )
    return list(users)


async def get_all_users(session: AsyncSession) -> list[User]:
    users = await session.scalars(select(User).where(User.deleted_at.is_(None)))
    return list(users)


async def get_user_with_roles(
    user_id: UUID,
    session: AsyncSession,
) -> User:
    user = await session.scalar(
        select(User)
        .options(
            load_only(
                User.id,
                User.is_active,
                User.deleted_at,
            ),
            selectinload(User.roles).load_only(
                Roles.id,
                Roles.name,
            ),
        )
        .where(User.id == user_id, User.deleted_at.is_(None), User.is_active == True)
    )
    return user if user else RaiseHttpException.check_is_exist(user)


async def update_user(
    session: AsyncSession,
    user_id: UUID,
    user_schema: ParticularUpdateUserSchema | UpdateUserSchema,
    particular: bool = False,
) -> User:
    user = await get_active_user_by_uuid(user_id=user_id, session=session)
    for key, value in user_schema.model_dump(exclude_unset=particular).items():
        setattr(user, key, value)
    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        if "email" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )
        elif "username" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this username already exists",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Duplicate entry for unique field",
            )
    return user


async def delete_user(session: AsyncSession, user_id: UUID) -> None:
    user = await get_user_by_uuid(user_id=user_id, session=session)
    user.is_active = False
    user.deleted_at = datetime.now(timezone.utc)
    await session.commit()
