from fastapi.routing import APIRouter

from app.auth import admin_depends
from app.db import SessionDepends
from app.schemes.currency import CurrenciesCodes, CurrenciesCreate
from app import crud

router = APIRouter(prefix="/currencies", tags=["currencies"])


@router.post("/", dependencies=[admin_depends], status_code=200)
async def add_currencies(
    db: SessionDepends, currencies_scheme: CurrenciesCreate
) -> CurrenciesCodes:
    existed, affected = await crud.currency.create_many(db, currencies_scheme)
    return CurrenciesCodes(existed_codes=existed, affected_codes=affected)
