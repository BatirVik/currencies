import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils import auth_client, create_currencies, generate_user


@pytest.mark.asyncio
async def test_get_currency(db: AsyncSession, client: TestClient):
    user_data = await generate_user(db)
    auth_client(client, user_data.email, user_data.password)
    await create_currencies(db, USD=1, EUR=1.12)
    resp = client.get("/v1/currencies/EUR")
    assert resp.status_code == 200
    assert resp.json() == {"code": "EUR", "equals_usd": "1.1200"}


@pytest.mark.asyncio
async def test_get_currency__unauthorized(db: AsyncSession, client: TestClient):
    await create_currencies(db, USD=1, EUR=1.12)
    resp = client.get("/v1/currencies/EUR")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_get_currency__not_found(db: AsyncSession, client: TestClient):
    user_data = await generate_user(db, is_admin=True)
    auth_client(client, user_data.email, user_data.password)
    await create_currencies(db, USD=1)
    resp = client.get("/v1/currencies/EUR")
    assert resp.status_code == 404
