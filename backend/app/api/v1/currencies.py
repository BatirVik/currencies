from typing import Annotated
from fastapi import HTTPException, APIRouter, Path

from app.auth import admin_depends
from app.db import SessionDepends
from app.schemes.currency import (
    CurrenciesList,
    CurrenciesUpdateResp,
    CurrenciesUpsertResp,
    CurrenciesCreateResp,
    CurrencyCodesList,
    CurrencyRead,
)
from app import crud
from app.models.currency import Currency

router = APIRouter(prefix="/currencies", tags=["currencies"])


@router.get("/", response_model=CurrenciesList)
async def get_all_currencies(db: SessionDepends) -> dict:
    currs = await crud.currency.read_all(db)
    return {"currencies": currs}


@router.get("/codes")
async def get_available_currency_codes(db: SessionDepends) -> CurrencyCodesList:
    codes = await crud.currency.read_all_codes(db)
    return CurrencyCodesList(codes=codes)


@router.get("/{code}", response_model=CurrencyRead)
async def get_currency(
    db: SessionDepends, code: Annotated[str, Path(min_length=3, max_length=3)]
) -> Currency:
    if currency := await crud.currency.read(db, code):
        return currency
    raise HTTPException(404, "Currency not found")


@router.delete("/{code}", status_code=204, dependencies=[admin_depends])
async def remove_currency(
    db: SessionDepends, code: Annotated[str, Path(min_length=3, max_length=3)]
) -> None:
    if await crud.currency.delete(db, code):
        return
    raise HTTPException(404, "Currency not found")


@router.post("/", dependencies=[admin_depends], status_code=201)
async def add_currencies(
    db: SessionDepends, currs_scheme: CurrenciesList
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
    db: SessionDepends, currs_scheme: CurrenciesList
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


@router.put("/", dependencies=[admin_depends], status_code=200)
async def upsert_currencies(
    db: SessionDepends, currs_scheme: CurrenciesList
) -> CurrenciesUpsertResp:
    res = await crud.currency.upsert_many(db, currs_scheme)
    return CurrenciesUpsertResp(
        created_codes=res.created_codes,
        updated_codes=res.updated_codes,
    )
