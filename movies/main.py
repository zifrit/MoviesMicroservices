import logging

import uvicorn
from fastapi import FastAPI
from src.utils.logger import LOGGING
from src.core.settings import settings


app = FastAPI(
    title=settings.PROJECT_TITLE,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=8002,
        reload=True,
        log_level=logging.DEBUG,
        log_config=LOGGING,
    )
