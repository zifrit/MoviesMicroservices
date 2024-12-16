from fastapi import Depends, APIRouter, Response, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.redis import RedisCache, get_redis
from src.db.session import db_session
from src.services.validate_auth_user import validate_auth_user
from src.utils.auth_utils import auth_utils
from src.schemas.permissions import RolesSchema

router = APIRouter()
http_bearer = HTTPBearer(auto_error=True)


@router.post("/login")
async def login(
    user=Depends(validate_auth_user),
) -> dict[str, str]:
    payload = {
        "sub": user.username,
        "roles": [RolesSchema.model_validate(role).name for role in user.roles],
        "user_id": str(user.id),
    }
    access_token, refresh_token = await auth_utils.create_jwt_token(payload=payload)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }


@router.post("/logout", dependencies=[Depends(auth_utils.get_current_active_user)])
async def logout(
    cache: RedisCache = Depends(get_redis),
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
) -> Response:
    await auth_utils.logout(cache=cache, token=token.credentials)
    return Response(status_code=status.HTTP_200_OK)


@router.post("/refresh")
async def logout(
    token: str,
    cache: RedisCache = Depends(get_redis),
    session: AsyncSession = Depends(db_session.get_session),
) -> dict[str, str]:
    access_token, refresh_token = await auth_utils.refreshed_jwt_token(
        cache=cache,
        token=token,
        session=session,
    )
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
