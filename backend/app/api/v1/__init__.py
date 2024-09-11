from fastapi.routing import APIRouter
from . import currencies, users

router = APIRouter(prefix="/v1")
router.include_router(users.router)
