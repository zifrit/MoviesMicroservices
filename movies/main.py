import logging

import uvicorn
from fastapi import FastAPI
from src.utils.logger import LOGGING
from src.core.settings import settings
from src.api.v1 import movies

app = FastAPI(
    title=settings.PROJECT_TITLE,
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
)

app.include_router(movies.router, prefix="/api/movies", tags=["movies"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=8002,
        reload=True,
        log_level=logging.DEBUG,
        log_config=LOGGING,
    )
