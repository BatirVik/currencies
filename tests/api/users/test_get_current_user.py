import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.testclient import TestClient

from tests.utils import auth_client, generate_user


@pytest.mark.asyncio
async def test_get_current_user(db: AsyncSession, client: TestClient):
    user_data = await generate_user(db)
    auth_client(client, user_data.email, user_data.password)
    resp = client.get("/v1/users/me")
    assert resp.status_code == 200
    resp_data = resp.json()
    assert resp_data.keys() == {"id", "is_admin", "email"}
    assert resp_data["email"] == user_data.email
