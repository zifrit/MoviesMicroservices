import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from redis.asyncio import Redis

from src.db import redis
from src.utils.logger import LOGGING
from src.core.settings import settings
from src.api.v1 import user, login, permissions


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        redis.redis = Redis(
            host=settings.redis_settings.REDIS_HOST,
            port=settings.redis_settings.REDIS_PORT,
        )
        yield
    finally:
        await redis.redis.close()


app = FastAPI(
    title=settings.PROJECT_TITLE,
    docs_url="/auth/api/openapi",
    openapi_url="/auth/api/openapi.json",
    lifespan=lifespan,
)

app.include_router(user.router, prefix="/auth/api/users", tags=["users"])
app.include_router(login.router, prefix="/auth/api", tags=["login"])
app.include_router(permissions.router, prefix="/auth/api/roles", tags=["roles"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=8001,
        reload=True,
        log_level=logging.DEBUG,
        log_config=LOGGING,
    )
