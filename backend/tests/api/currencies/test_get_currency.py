import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils import create_currencies


@pytest.mark.asyncio
async def test_get_currency(db: AsyncSession, client: TestClient):
    await create_currencies(db, USD=1, EUR=1.12)
    resp = client.get("/v1/currencies/EUR")
    assert resp.status_code == 200
    assert resp.json() == {"code": "EUR", "equals_usd": "1.12"}


@pytest.mark.asyncio
async def test_get_currency_not_found(db: AsyncSession, client: TestClient):
    await create_currencies(db, USD=1)
    resp = client.get("/v1/currencies/EUR")
    assert resp.status_code == 404
