import jwt
from src.core.settings import settings
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from src.schemas.users import UserSchema

jwt_settings = settings.jwt_settings
http_bearer = HTTPBearer(auto_error=True)


class JWTUtils:

    @staticmethod
    def decode_token(
        token: str | bytes,
        key: str = jwt_settings.jwt_public_key.read_text(),
        algorithm: str = jwt_settings.ALGORITHM,
    ):
        try:
            encode = jwt.decode(
                jwt=token,
                key=key,
                algorithms=[algorithm],
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )
        return encode


class AuthUtils:
    @staticmethod
    async def get_current_user(
        token: HTTPAuthorizationCredentials = Depends(http_bearer),
    ) -> UserSchema:
        payload = JWTUtils.decode_token(token.credentials)
        user = UserSchema(username=payload["sub"], user_id=payload["user_id"])
        if user:
            return user
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


auth_utils = AuthUtils()
jwt_utils = JWTUtils()
