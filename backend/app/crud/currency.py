from typing import NamedTuple
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy.dialects.postgresql as postgresql
from sqlalchemy import sql, func

from app.models.currency import Currency
from app.schemes.currency import CurrenciesCreate, CurrenciesUpdate, CurrenciesUpsert


async def read(db: AsyncSession, code: str) -> Currency | None:
    return await db.get(Currency, code.upper())


class CreateManyResult(NamedTuple):
    existed_codes: list[str]
    created_codes: list[str]


async def create_many(
    db: AsyncSession, currencies_scheme: CurrenciesCreate
) -> CreateManyResult:
    codes = (curr.code for curr in currencies_scheme.currencies)
    curr_values = [curr.model_dump() for curr in currencies_scheme.currencies]
    stmt = sql.insert(Currency).values(curr_values).returning(Currency.code)
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


class UpsertManyResult(NamedTuple):
    created_codes: list[str]
    updated_codes: list[str]


async def upsert_many(
    db: AsyncSession, currencies_scheme: CurrenciesUpsert
) -> UpsertManyResult:
    curr_values = [curr.model_dump() for curr in currencies_scheme.currencies]
    stmt = postgresql.insert(Currency).values(curr_values)
    stmt = stmt.on_conflict_do_update(
        index_elements=["code"],
        set_={
            "equals_usd": stmt.excluded.equals_usd,
            "updated_at": func.now(),  # wont automatic refresh updated_at
        },
    )
    stmt = stmt.returning(Currency.code, Currency.created_at, Currency.updated_at)
    res = await db.execute(stmt)
    await db.commit()

    created_codes = []
    updated_codes = []

    for code, created_at, updated_at in res:
        if created_at == updated_at:
            created_codes.append(code)
        else:
            updated_codes.append(code)

    return UpsertManyResult(
        created_codes=created_codes,
        updated_codes=updated_codes,
    )
