from datetime import datetime, timezone
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy import DateTime, func
from uuid import UUID, uuid4


class Base(DeclarativeBase):
    __abstract__ = True

    repr_columns = ["id"]

    def __repr__(self) -> str:
        cols = []
        for col in self.repr_columns:
            cols.append(f"{col}={getattr(self, col)}")
        return " ".join(cols)


class CUDMixin(Base):
    __abstract__ = True
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class IdMixin(Base):
    __abstract__ = True
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, default=uuid4
    )


class IdCUDMixin(CUDMixin, IdMixin):
    __abstract__ = True
