from datetime import datetime, timezone
from uuid import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from sqlalchemy import String, Boolean, UniqueConstraint, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import BYTEA
from src.models.base import IdCUDMixin, Base

if TYPE_CHECKING:
    from src.models.roles import Roles


class User(IdCUDMixin):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String(255), unique=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[bytes] = mapped_column(BYTEA)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="true"
    )
    is_admin: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default="false"
    )
    roles: Mapped[list["Roles"]] = relationship(
        secondary="association_users_roles",
        back_populates="users",
    )


class AssociationUsersRoles(Base):
    __tablename__ = "association_users_roles"
    __table_args__ = (
        UniqueConstraint("role_id", "user_id", name="idx_unique_users_roles"),
    )
    id: Mapped[int] = mapped_column(primary_key=True)
    role_id: Mapped[UUID] = mapped_column(ForeignKey("roles.id"))
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=datetime.now(timezone.utc),
    )
