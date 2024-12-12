from fastapi import Depends, APIRouter

from src.services.validate_auth_user import validate_auth_user
from src.utils.auth_utils import jwt_utils
from src.schemas.permissions import RolesSchema

router = APIRouter()


@router.post("/login")
async def login(
    user=Depends(validate_auth_user),
):
    payload = {
        "sub": user.username,
        "roles": [RolesSchema.model_validate(role).name for role in user.roles],
    }
    access_token, refresh_token = jwt_utils.create_jwt_token(payload=payload)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
