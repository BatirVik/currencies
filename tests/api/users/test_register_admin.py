import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app import crud
from app.schemes.user import UserCreate

from tests.utils import generate_user, auth_client


@pytest.mark.asyncio
async def test_register_admin(db: AsyncSession, client: TestClient):
    user_data = await generate_user(db, is_admin=True)
    auth_client(client, user_data.email, user_data.password)

    resp = client.post(
        "v1/users/admin",
        json={"email": "user@gmail.com", "password": "12kj4H!090"},
    )
    assert resp.status_code == 201
    resp_data = resp.json()
    assert resp_data.keys() == {"id", "email", "is_admin"}
    user = await db.get(User, resp_data["id"])
    assert user
    assert user.is_admin


@pytest.mark.asyncio
async def test_register_admin__forbidden(db: AsyncSession, client: TestClient):
    user_data = await generate_user(db)
    auth_client(client, user_data.email, user_data.password)

    resp = client.post(
        "v1/users/admin",
        json={"email": "user@gmail.com", "password": "12kj4H!090"},
    )
    assert resp.status_code == 403

    stmt = select(User).where(User.email == "user@gmail.com").limit(1)
    user = await db.scalar(stmt)
    assert user is None


@pytest.mark.asyncio
async def test_register_user__conflict(db: AsyncSession, client: TestClient):
    user_data = await generate_user(db, is_admin=True)
    auth_client(client, user_data.email, user_data.password)

    await crud.user.create(
        db, UserCreate(email="user@gmail.com", password="12kj%%%!090")
    )
    resp = client.post(
        "v1/users/admin", json={"email": "user@gmail.com", "password": "12kj4H!090"}
    )
    assert resp.status_code == 409
