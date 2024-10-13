from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

from app import api
from app.logger import logger_middleware

app = FastAPI()
app.include_router(api.v1.router)

logger.remove(0)  # remove default logger
app.middleware("http")(logger_middleware)

DIST_PATH = Path(__file__).parent.parent.parent / "frontend" / "dist"

app.mount("/static", StaticFiles(directory=str(DIST_PATH)), name="static")


@app.get("/")
async def index_page():
    return FileResponse(DIST_PATH / "index.html", media_type="text/html")
