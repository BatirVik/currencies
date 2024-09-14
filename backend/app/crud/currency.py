from typing import NamedTuple
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy.dialects.postgresql as postgresql
from sqlalchemy import sql

from app.models.currency import Currency
from app.schemes.currency import CurrenciesCreate, CurrenciesUpdate, CurrenciesUpsert


class CreateManyResult(NamedTuple):
    existed_codes: list[str]
    created_codes: list[str]


async def create_many(
    db: AsyncSession, currencies_scheme: CurrenciesCreate
) -> CreateManyResult:
    codes = (curr.code for curr in currencies_scheme.currencies)
    curr_values = [curr.model_dump() for curr in currencies_scheme.currencies]
    stmt = postgresql.insert(Currency).values(curr_values).returning(Currency.code)
    try:
        created_codes = list(await db.scalars(stmt))
    except IntegrityError:
        await db.rollback()
        stmt = sql.select(Currency.code).where(Currency.code.in_(codes))
        exist_codes = list(await db.scalars(stmt))
        return CreateManyResult(exist_codes, [])
    await db.commit()
    return CreateManyResult([], created_codes)


class UpdateManyResult(NamedTuple):
    not_existed_codes: list[str]
    updated_codes: list[str]


async def update_many(
    db: AsyncSession, currencies_scheme: CurrenciesUpdate
) -> UpdateManyResult:
    codes = {curr.code for curr in currencies_scheme.currencies}
    stmt = sql.select(Currency.code).where(Currency.code.in_(codes)).with_for_update()
    existed_codes = set(await db.scalars(stmt))
    if len(existed_codes) != len(codes):
        return UpdateManyResult(list(codes.difference(existed_codes)), [])

    for curr in currencies_scheme.currencies:
        stmt = (
            sql.update(Currency)
            .where(Currency.code == curr.code)
            .values(equals_usd=curr.equals_usd)
        )
        await db.execute(stmt)
    await db.commit()
    return UpdateManyResult([], list(codes))


# async def update_many()
#     db: AsyncSession, currencies_scheme: CurrenciesUpsert
# ) -> UpdateManyResult:
#     """Returns (created_codes, updated_codes)"""
