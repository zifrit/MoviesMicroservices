from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from sqlalchemy import String, DateTime, ForeignKey, UniqueConstraint, func
from src.models.base import Base, IdCUDMixin


class Roles(IdCUDMixin):
    __tablename__ = "roles"
    name: Mapped[str] = mapped_column(String(255), unique=True)
    role_permissions: Mapped[list["RolePermissions"]] = relationship(
        secondary="association_roles_role_permissions",
        back_populates="roles",
    )


class RolePermissions(IdCUDMixin):
    __tablename__ = "role_permissions"
    name: Mapped[str] = mapped_column(String(255), unique=True)
    roles: Mapped[list["Roles"]] = relationship(
        secondary="association_roles_role_permissions",
        back_populates="role_permissions",
    )


class AssociationRolesRolePermissions(Base):
    __tablename__ = "association_roles_role_permissions"
    __table_args__ = (
        UniqueConstraint(
            "role_id", "role_permissions_id", name="idx_unique_roles_role_permissions"
        ),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[UUID] = mapped_column(ForeignKey("roles.id"))
    role_permissions_id: Mapped[UUID] = mapped_column(ForeignKey("role_permissions.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=datetime.now(timezone.utc),
    )
