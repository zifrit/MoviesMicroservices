from fastapi import APIRouter, Depends, status, Path, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from uuid import UUID

from src.utils.auth_utils import auth_utils
from src.db.session import db_session
from src.models.permissions import Roles, Permissions
from src.schemas.permissions import (
    CreateRolesSchema,
    CreatePermissionSchema,
    UpdateRolesSchema,
    UpdatePermissionSchema,
    ParticularUpdateRolesSchema,
    ParticularUpdatePermissionSchema,
    ShowRoleSchema,
    ShowPermissionSchema,
    ShowRolePermissionsSchema,
)
from src.services.crud import permissions as crud_permissions


router = APIRouter()


@router.post(
    "/",
    response_model=ShowRoleSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(auth_utils.get_current_active_user)],
)
async def create_role(
    role_schema: CreateRolesSchema,
    session: AsyncSession = Depends(db_session.get_session),
) -> Roles:
    return await crud_permissions.create_role(session=session, role_schema=role_schema)


@router.get(
    "/",
    response_model=list[ShowRoleSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(auth_utils.get_current_active_user)],
)
async def get_role(
    session: AsyncSession = Depends(db_session.get_session),
) -> list[Roles]:
    return await crud_permissions.get_roles(session=session)


@router.get(
    "/permissions",
    response_model=list[ShowPermissionSchema],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(auth_utils.get_current_active_user)],
)
async def get_permissions(
    session: AsyncSession = Depends(db_session.get_session),
) -> list[Permissions]:
    return await crud_permissions.get_permissions(session=session)


@router.get(
    "/{role_id}",
    response_model=ShowRoleSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(auth_utils.get_current_active_user)],
)
async def get_role(
    role_id: Annotated[UUID, Path],
    session: AsyncSession = Depends(db_session.get_session),
) -> Roles:
    return await crud_permissions.get_role(session=session, role_id=role_id)


@router.put(
    "/{role_id}",
    response_model=ShowRoleSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(auth_utils.get_current_active_user)],
)
async def update_role(
    role_id: Annotated[UUID, Path],
    role_schema: UpdateRolesSchema,
    session: AsyncSession = Depends(db_session.get_session),
) -> Roles:
    return await crud_permissions.update_role(
        session=session,
        role_id=role_id,
        role_schema=role_schema,
    )


@router.patch(
    "/{role_id}",
    response_model=ShowRoleSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(auth_utils.get_current_active_user)],
)
async def update_role(
    role_id: Annotated[UUID, Path],
    role_schema: ParticularUpdateRolesSchema,
    session: AsyncSession = Depends(db_session.get_session),
) -> Roles:
    return await crud_permissions.update_role(
        session=session, role_id=role_id, role_schema=role_schema, particular=True
    )


@router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(auth_utils.get_current_active_user)],
)
async def delete_role(
    role_id: Annotated[UUID, Path],
    session: AsyncSession = Depends(db_session.get_session),
) -> Response:
    await crud_permissions.delete_role(session=session, role_id=role_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{role_id}/add_permissions",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(auth_utils.get_current_active_user)],
)
async def add_permission_to_role(
    role_id: Annotated[UUID, Path],
    permissions_ids: set[UUID],
    session: AsyncSession = Depends(db_session.get_session),
) -> Response:
    await crud_permissions.add_permission_to_role(
        session=session, role_id=role_id, permissions_ids=permissions_ids
    )
    return Response(status_code=status.HTTP_200_OK)


@router.get(
    "/{role_id}/permissions",
    response_model=ShowRolePermissionsSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(auth_utils.get_current_active_user)],
)
async def get_role_permissions(
    role_id: Annotated[UUID, Path],
    session: AsyncSession = Depends(db_session.get_session),
) -> Roles:
    return await crud_permissions.get_role_permissions(session=session, role_id=role_id)


@router.post(
    "/permissions",
    response_model=ShowPermissionSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(auth_utils.get_current_active_user)],
)
async def create_permissions(
    role_permission_schema: CreatePermissionSchema,
    session: AsyncSession = Depends(db_session.get_session),
) -> Permissions:
    return await crud_permissions.create_permission(
        session=session, role_permission_schema=role_permission_schema
    )


@router.get(
    "/permissions/{permission_id}",
    response_model=ShowPermissionSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(auth_utils.get_current_active_user)],
)
async def get_permission(
    permission_id: Annotated[UUID, Path],
    session: AsyncSession = Depends(db_session.get_session),
) -> Permissions:
    return await crud_permissions.get_permission(
        session=session, permission_id=permission_id
    )


@router.put(
    "/permissions/{permission_id}",
    response_model=ShowPermissionSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(auth_utils.get_current_active_user)],
)
async def update_permissions(
    permission_id: Annotated[UUID, Path],
    permission_schema: UpdatePermissionSchema,
    session: AsyncSession = Depends(db_session.get_session),
) -> Permissions:
    return await crud_permissions.update_permission(
        session=session,
        permission_id=permission_id,
        permission_schema=permission_schema,
    )


@router.patch(
    "/permissions/{permission_id}",
    response_model=ShowPermissionSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(auth_utils.get_current_active_user)],
)
async def update_permissions(
    permission_id: Annotated[UUID, Path],
    permission_schema: ParticularUpdatePermissionSchema,
    session: AsyncSession = Depends(db_session.get_session),
) -> Permissions:
    return await crud_permissions.update_permission(
        session=session,
        permission_id=permission_id,
        permission_schema=permission_schema,
        particular=True,
    )


@router.delete(
    "/permissions/{permission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(auth_utils.get_current_active_user)],
)
async def delete_permissions(
    permission_id: Annotated[UUID, Path],
    session: AsyncSession = Depends(db_session.get_session),
) -> Response:
    await crud_permissions.delete_permission(
        permission_id=permission_id, session=session
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
