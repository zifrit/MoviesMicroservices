import logging
from fastapi import Depends, APIRouter

from src.core.settings import settings
from src.services.validate_auth_user import validate_auth_user
from src.utils.auth_utils import jwt_utils

router = APIRouter()


@router.post("/login")
async def login(
    user=Depends(validate_auth_user),
):
    payload = {
        "sub": user.username,
    }
    access_token, refresh_token = jwt_utils.create_jwt_token(payload=payload)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
