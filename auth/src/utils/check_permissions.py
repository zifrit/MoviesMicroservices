from functools import wraps
from fastapi import HTTPException, status, Request
from typing import Callable
from src.utils.auth_utils import jwt_utils


def check_permissions(required_role: str):
    def decorator(endpoint: Callable):
        @wraps(endpoint)
        async def wrapper(*args, **kwargs):
            request: Request = kwargs.get("request")
            if not request:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Request object is required",
                )

            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Missing or invalid Authorization header",
                )

            token = auth_header.split(" ")[1]
            payload = jwt_utils.decode_token(token)
            user_role = payload.get("roles")

            if required_role not in user_role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access forbidden: insufficient permissions",
                )

            return await endpoint(*args, **kwargs)

        return wrapper

    return decorator
