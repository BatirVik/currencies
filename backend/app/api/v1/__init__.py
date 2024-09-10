from fastapi.routing import APIRouter
from . import currencies

router = APIRouter(prefix='/v1')
router.include_router(currencies.router)
