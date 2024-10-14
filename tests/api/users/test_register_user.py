from fastapi.testclient import TestClient
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app import crud
from app.schemes.user import UserCreate


@pytest.mark.asyncio
async def test_register_user(db: AsyncSession, client: TestClient):
    resp = client.post(
        "v1/users",
        json={"email": "user@gmail.com", "password": "12kj4H!090"},
    )
    assert resp.status_code == 201
    resp_data = resp.json()
    assert resp_data.keys() == {"id", "email", "is_admin"}
    user = await db.get(User, resp_data["id"])
    assert user
    assert user.is_admin is False


@pytest.mark.asyncio
async def test_register_user__forbidden(db: AsyncSession, client: TestClient):
    await crud.user.create(
        db, UserCreate(email="user@gmail.com", password="12kj%%%!090")
    )
    resp = client.post(
        "v1/users", json={"email": "user@gmail.com", "password": "12kj4H!090"}
    )
    assert resp.status_code == 409
