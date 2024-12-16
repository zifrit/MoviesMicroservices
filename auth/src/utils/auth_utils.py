from datetime import timedelta, datetime, timezone
from uuid import uuid4

import bcrypt
import jwt
from src.core.settings import settings, JWTSettings
from src.db.redis import RedisCache, get_redis
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.db.session import db_session
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User
from src.schemas.permissions import RolesSchema
from src.services.crud import user as crud_user

jwt_settings = settings.jwt_settings
http_bearer = HTTPBearer(auto_error=True)


class AuthUtils:

    @staticmethod
    async def create_jwt_token(
        payload: dict,
        key: str = jwt_settings.jwt_private_key.read_text(),
        algorithm: str = jwt_settings.ALGORITHM,
        access_expire_minutes: int = jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        refresh_expire_minutes: int = jwt_settings.REFRESH_TOKEN_EXPIRE_MINUTES,
        access_expires_delta: timedelta | None = None,
        refresh_expires_delta: timedelta | None = None,
    ) -> tuple[str, str]:
        access_payload = payload.copy()
        refresh_payload = payload.copy()
        refresh_payload.pop("roles")
        refresh_payload.pop("user_id")

        now = datetime.now(timezone.utc)
        jti_refresh = str(uuid4())
        jti_access = str(uuid4())

        if access_expires_delta:
            exp = now + access_expires_delta
        else:
            exp = now + timedelta(minutes=access_expire_minutes)
        access_payload.update(
            exp=exp,
            iat=now,
            type="access_token",
            jti_refresh=jti_refresh,
            jti_access=jti_access,
        )

        if refresh_expires_delta:
            exp = now + refresh_expires_delta
        else:
            exp = now + timedelta(minutes=refresh_expire_minutes)
        refresh_payload.update(
            exp=exp,
            iat=now,
            type="refresh_token",
            jti_refresh=jti_refresh,
        )

        access_token = jwt.encode(
            payload=access_payload,
            key=key,
            algorithm=algorithm,
        )
        refresh_token = jwt.encode(
            payload=refresh_payload,
            key=key,
            algorithm=algorithm,
        )
        return access_token, refresh_token

    @staticmethod
    async def refreshed_jwt_token(
        token: str,
        cache: RedisCache = Depends(get_redis),
        session: AsyncSession = Depends(db_session.get_session),
    ) -> tuple[str, str]:
        decoded_token = await AuthUtils.decode_token(token=token)
        if decoded_token["type"] != "refresh_token":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token not refresh",
            )
        if await cache.get(decoded_token["jti_refresh"]):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Token is in black list"
            )

        user: User = await crud_user.get_active_user_by_username_with_roles(
            username=decoded_token["sub"], session=session
        )
        payload = {
            "sub": user.username,
            "roles": [RolesSchema.model_validate(role).name for role in user.roles],
            "user_id": str(user.id),
        }
        return await AuthUtils.create_jwt_token(payload=payload)

    @staticmethod
    async def decode_token(
        token: str | bytes,
        key: str = jwt_settings.jwt_public_key.read_text(),
        algorithm: str = jwt_settings.ALGORITHM,
        cache: RedisCache = Depends(get_redis),
    ) -> dict:
        try:
            encode = jwt.decode(
                jwt=token,
                key=key,
                algorithms=[algorithm],
            )
            if await cache.get(encode["access_token"]):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Token is in black list",
                )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        return encode

    @staticmethod
    def hash_password(password: str) -> bytes:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    @staticmethod
    def check_password(password: str, hashed_password: bytes) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password)

    @staticmethod
    async def get_current_active_user(
        session: AsyncSession = Depends(db_session.get_session),
        token: HTTPAuthorizationCredentials = Depends(http_bearer),
    ) -> User:
        payload = await AuthUtils.decode_token(token.credentials)
        if payload["type"] != "access_token":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token not access",
            )
        user = await crud_user.get_active_user_by_username_with_roles(
            username=payload["sub"], session=session
        )
        if user:
            return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


auth_utils = AuthUtils()
