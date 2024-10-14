import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.currency import Currency
from tests.utils import create_currencies, generate_user, auth_client


@pytest.mark.asyncio
async def test_remove_currency(db: AsyncSession, client: TestClient):
    user_data = await generate_user(db, is_admin=True)
    auth_client(client, user_data.email, user_data.password)

    await create_currencies(db, USD=1, EUR=1.12)
    resp = client.delete("/v1/currencies/EUR")
    assert resp.status_code == 204

    db_codes = set(await db.scalars(select(Currency.code)))
    assert db_codes == {"USD"}


@pytest.mark.asyncio
async def test_remove_currency__forbidden(db: AsyncSession, client: TestClient):
    user_data = await generate_user(db)
    auth_client(client, user_data.email, user_data.password)

    await create_currencies(db, USD=1, EUR=1.12)
    resp = client.delete("/v1/currencies/EUR")
    assert resp.status_code == 403

    db_codes = set(await db.scalars(select(Currency.code)))
    assert db_codes == {"USD", "EUR"}


@pytest.mark.asyncio
async def test_remove_currency_not_found(db: AsyncSession, client: TestClient):
    user_data = await generate_user(db, is_admin=True)
    auth_client(client, user_data.email, user_data.password)

    await create_currencies(db, USD=1)
    resp = client.delete("/v1/currencies/EUR")
    assert resp.status_code == 404
