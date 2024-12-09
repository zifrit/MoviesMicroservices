from sqlalchemy.orm import Mapped, mapped_column
from typing import TYPE_CHECKING
from sqlalchemy import String, Boolean
from sqlalchemy.dialects.postgresql import BYTEA
from src.models.base import Base


class User(Base):
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
