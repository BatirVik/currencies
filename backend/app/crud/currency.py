from collections.abc import Sequence

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
import sqlalchemy.dialects.postgresql as postgresql
from sqlalchemy import sql


from app.models.currency import Currency
from app.schemes.currency import CurrenciesCreate, CurrencyScheme


# async def _create_many_update(
#     db: AsyncSession, currency_schemes: Sequence[CurrencyScheme]
# ) -> tuple[set[str], set[str]]:
#     codes = {curr.code for curr in currency_schemes}
#     curr_values = [curr.model_dump() for curr in currency_schemes]

#     stmt = sql.select(Currency.code).where(Currency.code.in_(codes)).with_for_update()
#     existed_codes = set(await db.scalars(stmt))

#     stmt = postgresql.insert(Currency).values(curr_values)
#     stmt = stmt.on_conflict_do_update(
#         index_elements=["code"], set_={"equals_usd": stmt.excluded.equals_usd}
#     )
#     await db.execute(stmt)

#     await db.commit()
#     return existed_codes, codes


async def create_many(
    db: AsyncSession, currencies_scheme: CurrenciesCreate
) -> list[str]:
    """Returns existed codes"""
    codes = (curr.code for curr in currencies_scheme.currencies)
    curr_values = [curr.model_dump() for curr in currencies_scheme.currencies]
    stmt = postgresql.insert(Currency).values(curr_values)
    try:
        await db.execute(stmt)
    except IntegrityError:
        await db.rollback()
        stmt = sql.select(Currency.code).where(Currency.code.in_(codes))
        exist_codes = list(await db.scalars(stmt))
        return exist_codes
    await db.commit()
    return []


# def update_many(db: AsyncSession, currencies_scheme: CurrenciesCreate):
#     """Returns existed codes"""
