from collections.abc import Sequence

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy.dialects.postgresql as postgresql
from sqlalchemy import sql


from app.models.currency import Currency
from app.schemes.currency import CurrenciesCreate, CurrencyScheme


async def _create_many_abort(
    db: AsyncSession, currency_schemes: Sequence[CurrencyScheme]
) -> tuple[set[str], set[str]]:
    codes = (curr.code for curr in currency_schemes)
    curr_values = [curr.model_dump() for curr in currency_schemes]
    stmt = postgresql.insert(Currency).values(curr_values).returning(Currency.code)
    try:
        affected_codes = set(await db.scalars(stmt))
    except IntegrityError:
        await db.rollback()
        stmt = sql.select(Currency.code).where(Currency.code.in_(codes))
        exist_codes = set(await db.scalars(stmt))
        return exist_codes, set()
    await db.commit()
    return set(), affected_codes


async def _create_many_skip(
    db: AsyncSession, currency_schemes: Sequence[CurrencyScheme]
) -> tuple[set[str], set[str]]:
    codes = {curr.code for curr in currency_schemes}
    curr_values = [curr.model_dump() for curr in currency_schemes]
    stmt = (
        postgresql.insert(Currency)
        .values(curr_values)
        .on_conflict_do_nothing()
        .returning(Currency.code)
    )
    affected_codes = set(await db.scalars(stmt))

    await db.commit()
    return codes.difference(affected_codes), affected_codes


async def _create_many_update(
    db: AsyncSession, currency_schemes: Sequence[CurrencyScheme]
) -> tuple[set[str], set[str]]:
    codes = {curr.code for curr in currency_schemes}
    curr_values = [curr.model_dump() for curr in currency_schemes]

    stmt = sql.select(Currency.code).where(Currency.code.in_(codes)).with_for_update()
    existed_codes = set(await db.scalars(stmt))

    stmt = postgresql.insert(Currency).values(curr_values)
    stmt = stmt.on_conflict_do_update(
        index_elements=["code"], set_={"equals_usd": stmt.excluded.equals_usd}
    )
    await db.execute(stmt)

    await db.commit()
    return existed_codes, codes


async def create_many(
    db: AsyncSession, currencies_scheme: CurrenciesCreate
) -> tuple[set[str], set[str]]:
    """Returns (existed_codes, affected_codes)"""
    match currencies_scheme.on_presence:
        case "abort":
            return await _create_many_abort(db, currencies_scheme.currencies)
        case "skip":
            return await _create_many_skip(db, currencies_scheme.currencies)
        case "update":
            return await _create_many_update(db, currencies_scheme.currencies)
