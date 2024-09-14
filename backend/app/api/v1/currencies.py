from fastapi import HTTPException, APIRouter

from app.auth import admin_depends
from app.db import SessionDepends
from app.schemes.currency import (
    CurrenciesCreate,
    CurrenciesUpdate,
    CurrenciesUpdateResp,
    CurrenciesUpsertResp,
    CurrenciesCreateResp,
)
from app import crud

router = APIRouter(prefix="/currencies", tags=["currencies"])


@router.post("/", dependencies=[admin_depends], status_code=201)
async def add_currencies(
    db: SessionDepends, currs_scheme: CurrenciesCreate
) -> CurrenciesCreateResp:
    res = await crud.currency.create_many(db, currs_scheme)
    if not res.existed_codes:
        return CurrenciesCreateResp(created_codes=res.created_codes)
    raise HTTPException(
        409,
        {
            "msg": "Some currencies already exists",
            "existed_codes": res.existed_codes,
        },
    )


@router.patch("/", dependencies=[admin_depends], status_code=200)
async def update_currencies(
    db: SessionDepends, currs_scheme: CurrenciesUpdate
) -> CurrenciesUpdateResp:
    res = await crud.currency.update_many(db, currs_scheme)
    if not res.not_existed_codes:
        return CurrenciesUpdateResp(updated_codes=res.updated_codes)
    raise HTTPException(
        404,
        {
            "msg": "Some currencies are not found",
            "not_existed_codes": res.not_existed_codes,
        },
    )


# @router.put("/", dependencies=[admin_depends], status_code=200)
# async def upsert_currencies(
#     db: SessionDepends, currs_scheme: CurrenciesUpsert
# ) -> CurrenciesUpsertResp:
#     res = await crud.currency.upsert_many(db, currs_scheme)
#     return CurrenciesUpsertResp(
#         created_codes=res.created_codes,
#         updated_codes=res.updated_codes,
#     )
