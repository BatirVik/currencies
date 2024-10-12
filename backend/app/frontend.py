from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

DIST_PATH = Path(__file__).parent.parent.parent / "frontend" / "dist"

router = APIRouter()
router.mount("/static", StaticFiles(directory=str(DIST_PATH)), name="static")


@router.get("/")
async def index_page():
    return FileResponse(DIST_PATH / "index.html", media_type="text/html")
