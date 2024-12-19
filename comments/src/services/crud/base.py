from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import Type
from uuid import UUID

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.base import Base
from src.schemas.base import BaseSchema
from src.utils.raising_http_excp import RaiseHttpException


class ABCModelManager(ABC):
    @abstractmethod
    def get_by_id(self, *args, **kwargs):
        pass

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def create(self, *args, **kwargs):
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        pass


class ModelManager[
    Model: Base,
    GET: BaseSchema,
    POST: BaseSchema,
    PUT: BaseSchema,
    PATCH: BaseSchema,
](ABCModelManager):
    def __init__(self, model: Type[Model]):
        self._model = model

    async def get_by_id(
        self, session: AsyncSession, id_: int | UUID, *args, **kwargs
    ) -> GET:
        result = await session.scalar(
            Select(self._model).where(
                self._model.id == id_,
                self._model.deleted_at.is_(None),
            )
        )
        RaiseHttpException.check_is_exist(result)
        return result

    async def get(
        self,
        session: AsyncSession,
        page_size: int,
        page_number: int,
        *args,
        **kwargs,
    ) -> list[GET | None]:
        page_from = page_size * (page_number - 1)
        result = await session.scalars(
            Select(self._model)
            .where(
                self._model.deleted_at.is_(None),
            )
            .offset(page_from)
            .limit(page_size)
        )
        return list(result)

    async def create(
        self, session: AsyncSession, obj_schema: POST, *args, **kwargs
    ) -> GET:
        item = self._model(**obj_schema.model_dump())
        session.add(item)
        await session.commit()
        await session.refresh(item)
        return item

    async def update(
        self,
        session: AsyncSession,
        id_: int | UUID,
        obj_schema: PUT | PATCH,
        particular: bool = False,
        *args,
        **kwargs,
    ):
        item = await self.get_by_id(session, id_=id_)
        for key, value in obj_schema.model_dump(exclude_unset=particular).items():
            setattr(item, key, value)
        await session.commit()
        return item

    async def delete(self, session: AsyncSession, id_: int | UUID, *args, **kwargs):
        item = await self.get_by_id(session, id_=id_)
        item.deleted_at = datetime.now(timezone.utc)
        await session.commit()
