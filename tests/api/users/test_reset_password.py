import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.testclient import TestClient

from app.auth import authenticate_user

from tests.utils import auth_client, generate_user


@pytest.mark.asyncio
async def test_reset_password(db: AsyncSession, client: TestClient):
    user_data = await generate_user(db)
    auth_client(client, user_data.email, user_data.password)
    new_password = "12#teHjk!178"
    resp = client.patch(
        "/v1/users/me/reset-password",
        json={"old_password": user_data.password, "new_password": new_password},
    )
    assert resp.status_code == 204
    assert await authenticate_user(db, user_data.email, new_password)


@pytest.mark.asyncio
async def test_reset_password__unauthorized(db: AsyncSession, client: TestClient):
    new_password = "12#teHjk!178"
    resp = client.patch(
        "/v1/users/me/reset-password",
        json={"old_password": "12hellon&", "new_password": new_password},
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_reset_password__authentication_failed(
    db: AsyncSession, client: TestClient
):
    user_data = await generate_user(db)
    auth_client(client, user_data.email, user_data.password)
    new_password = "12#teHjk!178"
    resp = client.patch(
        "/v1/users/me/reset-password",
        json={"old_password": user_data.password + "!", "new_password": new_password},
    )
    assert resp.status_code == 400
    assert await authenticate_user(db, user_data.email, user_data.password)
