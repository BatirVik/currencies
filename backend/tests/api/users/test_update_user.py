import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.testclient import TestClient

from app import crud
from app.auth import authenticate_user
from app.models.user import User

from tests.utils import auth_client, generate_email, generate_user


@pytest.mark.asyncio
async def test_update_user(db: AsyncSession, client: TestClient):
    user_data = await generate_user(db, is_admin=True)
    auth_client(client, user_data.email, user_data.password)

    user = await db.get_one(User, user_data.id)

    new_password = "12345He&/"
    new_email = generate_email()
    resp = client.patch(
        f"/v1/users/{user.id}",
        json={
            "password": new_password,
            "email": new_email,
        },
    )
    assert resp.status_code == 200

    await db.refresh(user)

    assert await authenticate_user(db, user.email, new_password)
    assert resp.json() == {
        "id": str(user.id),
        "email": new_email,
        "is_admin": user.is_admin,
    }


@pytest.mark.asyncio
async def test_update_user_with_taken_email(db: AsyncSession, client: TestClient):
    user_data = await generate_user(db, is_admin=True)
    auth_client(client, user_data.email, user_data.password)

    user = await db.get_one(User, user_data.id)

    new_email = (await generate_user(db)).email
    resp = client.patch(f"/v1/users/{user.id}", json={"email": new_email})

    assert resp.status_code == 409

    await db.refresh(user)
    assert user.email == user_data.email


@pytest.mark.asyncio
async def test_not_admin_update_user(db: AsyncSession, client: TestClient):
    user_data = await generate_user(db)
    auth_client(client, user_data.email, user_data.password)

    user = await db.get_one(User, user_data.id)

    new_password = "12345He&/"
    new_email = generate_email()
    resp = client.patch(
        f"/v1/users/{user.id}",
        json={
            "password": new_password,
            "email": new_email,
        },
    )
    assert resp.status_code == 403
