from fastapi.routing import APIRouter
from . import users, auth, currencies

router = APIRouter(prefix="/v1")
router.include_router(users.router)
router.include_router(auth.router)
router.include_router(currencies.router)
