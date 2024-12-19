from fastapi import HTTPException
from starlette import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.base import Base


class RaiseHttpException:

    @staticmethod
    def check_is_exist(item) -> None:
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Not found"
            )

    @staticmethod
    async def check_is_not_delete(
        _models: dict, _ids: dict, session: AsyncSession
    ) -> None:
        errors = []
        for key, value in _ids.items():
            model: Base = _models.get(key)
            result = await session.scalar(
                select(model).where(model.id == value, model.deleted_at.is_(None))
            )
            if not result:
                errors.append({key: "Not exist"})
        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=errors
            )
