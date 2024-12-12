from uuid import UUID

from src.schemas.base import BaseSchema


class RolesSchema(BaseSchema):
    name: str


class CreateRolesSchema(RolesSchema):
    pass


class ShowRoleSchema(RolesSchema):
    id: UUID


class UpdateRolesSchema(RolesSchema):
    pass


class ParticularUpdateRolesSchema(BaseSchema):
    name: str | None = None


class PermissionSchema(BaseSchema):
    name: str


class CreatePermissionSchema(PermissionSchema):
    pass


class ShowPermissionSchema(PermissionSchema):
    id: UUID


class UpdatePermissionSchema(PermissionSchema):
    pass


class ParticularUpdatePermissionSchema(BaseSchema):
    name: str | None = None


class ShowRolePermissionsSchema(PermissionSchema):
    id: UUID
    name: str
    role_permissions: list[ShowPermissionSchema]
