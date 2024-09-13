from fastapi import HTTPException, APIRouter

from app.auth import admin_depends
from app.db import SessionDepends
from app.schemes.currency import CurrenciesCreate
from app import crud

router = APIRouter(prefix="/currencies", tags=["currencies"])


@router.post("/", dependencies=[admin_depends], status_code=204)
async def add_currencies(db: SessionDepends, currs_scheme: CurrenciesCreate) -> None:
    if existed_codes := await crud.currency.create_many(db, currs_scheme):
        raise HTTPException(
            409,
            {"msg": "Some currencies already exists", "existed_codes": existed_codes},
        )
