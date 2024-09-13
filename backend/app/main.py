from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from loguru import logger

from app.logger import logger_middleware
from app import api

app = FastAPI()
app.include_router(api.v1.router)

logger.remove(0)
app.middleware("http")(logger_middleware)


@app.get("/")
def redirect_to_docs():
    return RedirectResponse("/docs")