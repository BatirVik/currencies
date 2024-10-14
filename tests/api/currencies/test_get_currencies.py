import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils import auth_client, create_currencies, generate_user


@pytest.mark.asyncio
async def test_get_currencies(db: AsyncSession, client: TestClient):
    user_data = await generate_user(db, is_admin=True)
    auth_client(client, user_data.email, user_data.password)
    await create_currencies(db, USD=1, EUR=1.12)
    resp = client.get("/v1/currencies/")
    assert resp.status_code == 200
    resp_data = resp.json()
    assert resp_data.keys() == {"currencies"}
    currs_data = {
        curr["code"]: float(curr["equals_usd"]) for curr in resp_data["currencies"]
    }
    assert currs_data == {"USD": 1, "EUR": 1.1200}


@pytest.mark.asyncio
async def test_get_currencies__unauthorized(db: AsyncSession, client: TestClient):
    resp = client.get("/v1/currencies/")
    assert resp.status_code == 401
