import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from tests.utils import auth_client, create_currencies, generate_user
from app.models.currency import Currency


@pytest.mark.asyncio
async def test_add_currencies(db: AsyncSession, client: TestClient):
    user_data = await generate_user(db, is_admin=True)
    auth_client(client, user_data.email, user_data.password)

    await create_currencies(db, USD=1)
    resp = client.post(
        "/v1/currencies",
        json={
            "currencies": [
                {"code": "EUR", "equals_usd": 1.14},
                {"code": "HRK", "equals_usd": 0.14},
            ],
        },
    )
    assert resp.status_code == 201
    resp_data = resp.json()
    assert resp_data.keys() == {"created_codes"}
    assert set(resp_data["created_codes"]) == {"EUR", "HRK"}

    res = await db.execute(select(Currency.code, Currency.equals_usd))
    db_currs = {code: float(value) for code, value in res}
    assert db_currs == {"EUR": 1.14, "USD": 1, "HRK": 0.14}


@pytest.mark.asyncio
async def test_not_admin_add_currencies(db: AsyncSession, client: TestClient):
    user_data = await generate_user(db)
    auth_client(client, user_data.email, user_data.password)

    await create_currencies(db, USD=1)
    resp = client.post(
        "/v1/currencies",
        json={
            "currencies": [
                {"code": "EUR", "equals_usd": 1.14},
                {"code": "HRK", "equals_usd": 0.14},
            ],
        },
    )
    assert resp.status_code == 403

    res = await db.execute(select(Currency.code, Currency.equals_usd))
    db_currs = {code: float(value) for code, value in res}
    assert db_currs == {"USD": 1}


@pytest.mark.asyncio
async def test_add_currencies_conflict(db: AsyncSession, client: TestClient):
    user_data = await generate_user(db, is_admin=True)
    auth_client(client, user_data.email, user_data.password)

    await create_currencies(db, USD=1, EUR=1.12)
    resp = client.post(
        "/v1/currencies",
        json={
            "currencies": [
                {"code": "EUR", "equals_usd": 1.14},
                {"code": "HRK", "equals_usd": 0.14},
            ],
        },
    )
    assert resp.status_code == 409
    resp_data = resp.json()
    assert "detail" in resp_data
    assert resp_data["detail"].keys() == {"msg", "existed_codes"}
    existed_codes = resp_data["detail"]["existed_codes"]
    assert set(existed_codes) == {"EUR"}

    res = await db.execute(select(Currency.code, Currency.equals_usd))
    db_currs = {code: float(value) for code, value in res}
    assert db_currs == {"EUR": 1.12, "USD": 1}
