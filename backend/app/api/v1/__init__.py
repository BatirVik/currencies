from fastapi.routing import APIRouter
from . import users, auth

router = APIRouter(prefix="/v1")
router.include_router(users.router)
router.include_router(auth.router)
