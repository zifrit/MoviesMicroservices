import logging
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from src.db.session import db_session
from src.schemas.user import UserLoginSchema
from src.utils.auth_utils import jwt_utils
from src.services.crud import user as crud_user

router = APIRouter()

logger = logging.getLogger(__name__)


async def validate_auth_user(
    login_user: UserLoginSchema,
    session: AsyncSession = Depends(db_session.get_session),
):
    unauthed_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Username or password incorrect",
    )
    user = await crud_user.get_active_user_by_username(
        session=session, username=login_user.username
    )
    if not user:
        raise unauthed_exception
    if not (jwt_utils.check_password(login_user.password, user.password)):
        raise unauthed_exception
    return user
