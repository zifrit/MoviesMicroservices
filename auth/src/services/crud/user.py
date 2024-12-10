from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status, Path
from src.models.user import User

from src.schemas.user import (
    CreateUserSchema,
    UpdateUserSchema,
    ParticularUpdateUserSchema,
)
from src.utils.raising_http_excp import RaiseHttpException


async def create_user(
    user: CreateUserSchema,
    session: AsyncSession,
) -> User:
    new_user = User(**user.model_dump())
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


async def get_active_user_by_uuid(session: AsyncSession, uuid: UUID = Path()) -> User:
    user = await session.scalar(
        select(User).where(User.id == uuid, User.is_active == True)
    )
    return user if user else RaiseHttpException.check_is_exist(user)


async def get_user_by_uuid(session: AsyncSession, uuid: UUID = Path()) -> User:
    user = await session.scalar(select(User).where(User.id == uuid))
    return user if user else RaiseHttpException.check_is_exist(user)


async def get_active_users(session: AsyncSession):
    return await session.scalars(
        select(User).where(User.is_active == True, User.deleted_at.is_(None))
    )


async def get_all_users(session: AsyncSession):
    return await session.scalars(select(User).where(User.deleted_at.is_(None)))


async def update_user(
    session: AsyncSession,
    user: User,
    user_schema: ParticularUpdateUserSchema | UpdateUserSchema,
    particular: bool = False,
) -> User:
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


async def delete_user(session: AsyncSession, user: User) -> None:
    user.is_active = False
    user.deleted_at = datetime.now(timezone.utc)
    await session.commit()
