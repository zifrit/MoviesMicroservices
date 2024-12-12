from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, load_only

from src.models.permissions import Roles, Permissions
from src.schemas.permissions import (
    CreateRolesSchema,
    CreatePermissionSchema,
    UpdateRolesSchema,
    UpdatePermissionSchema,
    ParticularUpdateRolesSchema,
    ParticularUpdatePermissionSchema,
)
from src.schemas.user import AddRoleToUserSchema
from src.utils.raising_http_excp import RaiseHttpException
from src.services.crud.user import get_user_with_roles


async def create_role(
    session: AsyncSession,
    role_schema: CreateRolesSchema,
) -> Roles:
    new_role = Roles(**role_schema.model_dump())
    try:
        session.add(new_role)
        await session.commit()
        await session.refresh(new_role)
    except IntegrityError as e:
        if "name" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role with this name already exists",
            )
    return new_role


async def get_role(
    session: AsyncSession,
    role_id: UUID,
) -> Roles:
    role = await session.scalar(
        select(Roles).where(Roles.id == role_id, Roles.deleted_at.is_(None))
    )
    return role if role else RaiseHttpException.check_is_exist(role)


async def get_roles(
    session: AsyncSession,
) -> list[Roles]:
    roles = await session.scalars(select(Roles).where(Roles.deleted_at.is_(None)))
    return list(roles)


async def update_role(
    session: AsyncSession,
    role_id: UUID,
    role_schema: UpdateRolesSchema | ParticularUpdateRolesSchema,
    particular: bool = False,
):
    role = await get_role(session=session, role_id=role_id)
    for key, value in role_schema.model_dump(exclude_unset=particular).items():
        setattr(role, key, value)
    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        if "name" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role with this name already exists",
            )
    return role


async def delete_role(
    session: AsyncSession,
    role_id: UUID,
) -> None:
    role = await get_role(session=session, role_id=role_id)
    role.deleted_at = datetime.now(timezone.utc)
    await session.commit()


async def create_permission(
    session: AsyncSession,
    role_permission_schema: CreatePermissionSchema,
) -> Permissions:
    new_permission = Permissions(**role_permission_schema.model_dump())
    try:
        session.add(new_permission)
        await session.commit()
        await session.refresh(new_permission)
    except IntegrityError as e:
        if "name" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Permission with this name already exists",
            )
    return new_permission


async def get_permissions(
    session: AsyncSession,
) -> list[Permissions]:
    permissions = await session.scalars(
        select(Permissions).where(Permissions.deleted_at.is_(None))
    )
    return list(permissions)


async def get_permission(
    session: AsyncSession,
    permission_id: UUID,
) -> Permissions:
    permission = await session.scalar(
        select(Permissions).where(
            Permissions.id == permission_id, Permissions.deleted_at.is_(None)
        )
    )
    return permission if permission else RaiseHttpException.check_is_exist(permission)


async def update_permission(
    session: AsyncSession,
    permission_id: UUID,
    permission_schema: UpdatePermissionSchema | ParticularUpdatePermissionSchema,
    particular: bool = False,
) -> Permissions:
    permission = await get_permission(session=session, permission_id=permission_id)
    for key, value in permission_schema.model_dump(exclude_unset=particular).items():
        setattr(permission, key, value)
    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        if "name" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Permission with this name already exists",
            )
    return permission


async def delete_permission(
    session: AsyncSession,
    permission_id: UUID,
) -> None:
    permission = await get_permission(session=session, permission_id=permission_id)
    permission.deleted_at = datetime.now(timezone.utc)
    await session.commit()


async def add_permission_to_role(
    session: AsyncSession,
    role_id: UUID,
    permissions_ids: set[UUID],
) -> None:
    role = await session.scalar(
        select(Roles)
        .options(selectinload(Roles.role_permissions))
        .where(Roles.id == role_id)
    )
    for permission_id in permissions_ids:
        permission = await get_permission(session=session, permission_id=permission_id)
        role.role_permissions.append(permission)
    await session.commit()


async def get_role_permissions(
    session: AsyncSession,
    role_id: UUID,
) -> Roles:
    role_with_permissions = await session.scalar(
        select(Roles)
        .options(
            load_only(Roles.id, Roles.name),
            selectinload(Roles.role_permissions).load_only(
                Permissions.name, Permissions.id
            ),
        )
        .where(Roles.id == role_id, Roles.deleted_at.is_(None))
    )
    RaiseHttpException.check_is_exist(role_with_permissions)
    return role_with_permissions


async def add_role_to_user(
    session: AsyncSession,
    user_id: UUID,
    role_id: AddRoleToUserSchema,
) -> None:
    user = await get_user_with_roles(session=session, user_id=user_id)
    role = await get_role(session=session, role_id=role_id.role_id)
    user.roles.append(role)
    await session.commit()
