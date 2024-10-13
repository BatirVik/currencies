from typing import Annotated
from fastapi import HTTPException, APIRouter, Path

from app.auth import admin_depends
from app.db import SessionDepends
from app.exceptions.currency import CurrencyNotFound
from app.schemes.currency import CurrenciesList, CurrencyRead, CurrenciesRead
from app import crud
from app.models.currency import Currency

router = APIRouter(prefix="/currencies", tags=["currencies"])


@router.get("/", response_model=CurrenciesRead)
async def get_all_currencies(db: SessionDepends) -> dict[str, list[Currency]]:
    currs = await crud.currency.read_all(db)
    return {"currencies": currs}


@router.get("/codes")
async def get_available_currency_codes(db: SessionDepends) -> dict[str, list[str]]:
    codes = await crud.currency.read_all_codes(db)
    return {"codes": codes}


@router.get("/{code}", response_model=CurrencyRead)
async def get_currency(
        db: SessionDepends, code: Annotated[str, Path(min_length=3, max_length=3)]
) -> Currency:
    try:
        return await crud.currency.read(db, code)
    except CurrencyNotFound:
        raise HTTPException(404, "Currency not found")


@router.delete("/{code}", status_code=204, dependencies=[admin_depends])
async def remove_currency(
        db: SessionDepends, code: Annotated[str, Path(min_length=3, max_length=3)]
) -> None:
    try:
        await crud.currency.delete(db, code)
    except CurrencyNotFound:
        raise HTTPException(404, "Currency not found")


@router.post("/", dependencies=[admin_depends], status_code=201)
async def add_currencies(
        db: SessionDepends, currs_scheme: CurrenciesList
) -> dict[str, list[str]]:
    res = await crud.currency.create_many(db, currs_scheme)
    if not res.existed_codes:
        return {
            "created_codes": res.created_codes,
        }
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
) -> dict[str, list[str]]:
    res = await crud.currency.update_many(db, currs_scheme)
    if not res.not_existed_codes:
        return {
            "updated_codes": res.updated_codes,
        }
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
) -> dict[str, list[str]]:
    res = await crud.currency.upsert_many(db, currs_scheme)
    return {
        "created_codes": res.created_codes,
        "updated_codes": res.updated_codes,
    }
