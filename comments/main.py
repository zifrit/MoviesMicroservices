import logging

import uvicorn
from fastapi import FastAPI
from src.utils.logger import LOGGING
from src.core.settings import settings
from src.api.v1 import comments

app = FastAPI(
    title=settings.PROJECT_TITLE,
    docs_url="/comments/api/openapi",
    openapi_url="/comments/api/openapi.json",
)

app.include_router(comments.router, prefix="/comments/api", tags=["comments"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=8003,
        reload=True,
        log_level=logging.DEBUG,
        log_config=LOGGING,
    )
