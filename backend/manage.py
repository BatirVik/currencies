import asyncio
import sys
from app import crud
from app.schemes.user import UserCreate
from app.schemes.currency import CurrenciesList, CurrencyScheme
from app.db import session_factory

from decimal import Decimal

currencies = {"USD": 1, "EUR": 1.11, "UAH": 0.02, "HRK": 0.14, "CAD": 0.74}


async def create_mock_currs():
    currs_scheme = CurrenciesList(
        currencies=[
            CurrencyScheme(code=code, equals_usd=Decimal(value))
            for code, value in currencies.items()
        ]
    )
    async with session_factory() as db:
        res = await crud.currency.create_many(db, currs_scheme)
    if res.existed_codes:
        print(
            f"Currencies not created beacause some of them already exists: {res.existed_codes!r}"
        )
    else:
        print(f"Created currencies codes: {res.created_codes!r}")


async def create_admin(email: str, password: str, is_admin: bool):
    async with session_factory() as db:
        user_scheme = UserCreate(email=email, password=password)
        user = await crud.user.create(db, user_scheme, is_admin=True)
        if user is None:
            print("Failed: email already taken")
        else:
            print("Success: created")


async def main() -> None:
    match sys.argv[1:]:
        case ["create-admin", email, password]:
            await create_admin(email, password, is_admin=True)
        case ["create-user", email, password]:
            await create_admin(email, password, is_admin=False)
        case ["create-mock-currs"]:
            await create_mock_currs()
        case _:
            print("Incorrect args!")


if __name__ == "__main__":
    asyncio.run(main())
