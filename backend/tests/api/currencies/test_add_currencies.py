from typing import Literal

import pytest
from pytest import FixtureRequest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.currency import Currency
from tests.utils import auth_client, create_currencies, generate_user


@pytest.fixture(params=["abort", "update", "skip"])
def on_presence(request: FixtureRequest) -> Literal["abort", "update", "skip"]:
    return request.param


@pytest.mark.asyncio
async def test_add_currencies(
    db: AsyncSession,
    client: TestClient,
    on_presence: Literal["abort", "update", "skip"],
):
    user_data = await generate_user(db, is_admin=True)
    auth_client(client, user_data.email, user_data.password)

    await create_currencies(db, EUR=1.12, USD=1)
    resp = client.post(
        "/v1/currencies",
        json={
            "on_presence": on_presence,
            "currencies": [
                {"code": "EUR", "equals_usd": 1.14},
                {"code": "HRK", "equals_usd": 0.14},
            ],
        },
    )
    assert resp.status_code == 200

    resp_data = resp.json()
    assert resp_data.keys() == {"existed_codes", "affected_codes"}
    existed_codes = set(resp_data["existed_codes"])
    affected_codes = set(resp_data["affected_codes"])

    res = await db.execute(select(Currency.code, Currency.equals_usd))
    db_curr_tuples = set((code, float(value)) for code, value in res)

    match on_presence:
        case "abort":
            assert existed_codes == {"EUR"}
            assert affected_codes == set()
            assert db_curr_tuples == {("EUR", 1.12), ("USD", 1)}
        case "skip":
            assert existed_codes == {"EUR"}
            assert affected_codes == {"HRK"}
            assert db_curr_tuples == {("EUR", 1.12), ("USD", 1), ("HRK", 0.14)}
        case "update":
            assert existed_codes == {"EUR"}
            assert affected_codes == {"EUR", "HRK"}
            assert db_curr_tuples == {("EUR", 1.14), ("USD", 1), ("HRK", 0.14)}


@pytest.mark.asyncio
async def test_add_currencies_abort(db: AsyncSession, client: TestClient):
    user_data = await generate_user(db, is_admin=True)
    auth_client(client, user_data.email, user_data.password)

    await create_currencies(db, EUR=1.12, USD=1)
    resp = client.post(
        "/v1/currencies",
        json={
            "on_presence": "abort",
            "currencies": [
                {"code": "HRK", "equals_usd": 0.14},
            ],
        },
    )
    assert resp.status_code == 200

    resp_data = resp.json()
    assert resp_data.keys() == {"existed_codes", "affected_codes"}
    assert set(resp_data["existed_codes"]) == set()
    assert set(resp_data["affected_codes"]) == {"HRK"}

    res = await db.execute(select(Currency.code, Currency.equals_usd))
    db_curr_tuples = set((code, float(value)) for code, value in res)

    assert db_curr_tuples == {("EUR", 1.12), ("USD", 1), ("HRK", 0.14)}


@pytest.mark.asyncio
async def test_not_admin_add_currencies(db: AsyncSession, client: TestClient):
    user_data = await generate_user(db)
    auth_client(client, user_data.email, user_data.password)

    await create_currencies(db, EUR=1.12, USD=1)
    resp = client.post(
        "/v1/currencies",
        json={
            "on_presence": "abort",
            "currencies": [
                {"code": "HRK", "equals_usd": 0.14},
            ],
        },
    )
    assert resp.status_code == 403

    res = await db.execute(select(Currency.code, Currency.equals_usd))
    db_curr_tuples = set((code, float(value)) for code, value in res)

    assert db_curr_tuples == {("EUR", 1.12), ("USD", 1)}
