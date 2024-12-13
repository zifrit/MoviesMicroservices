from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Integer
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from src.models.base import IdCUDMixin


class Movie(IdCUDMixin):
    __tablename__ = "movies"

    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[UUID] = mapped_column(Text)
    user_id: Mapped[int] = mapped_column(PG_UUID(as_uuid=True))
