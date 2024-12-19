import logging

import uvicorn
from fastapi import FastAPI
from src.utils.logger import LOGGING
from src.core.settings import settings
from src.api.v1 import movies

app = FastAPI(
    title=settings.PROJECT_TITLE,
    docs_url="/movies/api/openapi",
    openapi_url="/movies/api/openapi.json",
)

app.include_router(movies.router, prefix="/movies/api", tags=["movies"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=8002,
        reload=True,
        log_level=logging.DEBUG,
        log_config=LOGGING,
    )
