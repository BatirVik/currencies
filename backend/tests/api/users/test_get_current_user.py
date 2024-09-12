import pytest
import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.testclient import TestClient

from tests.utils import auth_client, generate_login_data


@pytest.mark.asyncio
async def test_get_current_user(db: AsyncSession, client: TestClient):
    email, psw = await generate_login_data(db, is_admin=True)
    auth_client(client, email, psw)
    resp = client.get("/v1/users/me")
    assert resp.status_code == 200
    resp_data = resp.json()
    assert resp_data.keys() == {"id", "is_admin", "email"}
    assert resp_data["email"] == email
