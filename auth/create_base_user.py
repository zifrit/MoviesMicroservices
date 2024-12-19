import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.user import User
from src.models.permissions import Roles
from src.utils.auth_utils import auth_utils
from src.db.session import db_session


async def create_user_role(session: AsyncSession) -> Roles:
    role = Roles(name="user")
    session.add(role)
    await session.commit()
    return role


async def create_base_user(session: AsyncSession) -> None:
    role = await create_user_role(session)
    new_user = User(
        username="admin",
        password=auth_utils.hash_password("admin"),
        email="admin@mail.ru",
    )
    session.add(new_user)
    await session.commit()

    user = await session.scalar(
        select(User).options(selectinload(User.roles)).where(User.username == "admin")
    )

    user.roles.append(role)
    await session.commit()


async def main() -> None:
    async with db_session.session_factory() as session:
        await create_base_user(session)


if __name__ == "__main__":
    asyncio.run(main())
