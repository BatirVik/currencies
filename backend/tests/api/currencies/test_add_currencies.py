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
    assert resp.status_code == 204

    res = await db.execute(select(Currency.code, Currency.equals_usd))
    db_curr_tuples = set((code, float(value)) for code, value in res)

    assert db_curr_tuples == {("EUR", 1.14), ("USD", 1), ("HRK", 0.14)}
