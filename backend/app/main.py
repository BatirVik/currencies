from fastapi import FastAPI
from loguru import logger

from app.logger import logger_middleware
from app import api, frontend

app = FastAPI()
app.include_router(frontend.router)
app.include_router(api.v1.router)

logger.remove(0)
app.middleware("http")(logger_middleware)
