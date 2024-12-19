from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from src.models.base import IdCUDMixin


class Comments(IdCUDMixin):
    __tablename__ = "comments"

    text: Mapped[UUID] = mapped_column(Text)
    object_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True))
    user_id: Mapped[int] = mapped_column(PG_UUID(as_uuid=True))
