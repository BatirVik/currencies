import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.utils import create_currencies


@pytest.mark.asyncio
async def test_get_currency_codes(db: AsyncSession, client: TestClient):
    await create_currencies(db, USD=1, EUR=1.12)
    resp = client.get("/v1/currencies/codes")
    assert resp.status_code == 200
    resp_data = resp.json()
    assert resp_data.keys() == {"codes"}
    assert set(resp_data["codes"]) == {"USD", "EUR"}
