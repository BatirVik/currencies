import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.testclient import TestClient
from sqlalchemy import select, exists

from app import crud
from app.models.user import User

from tests.utils import auth_client, generate_user


@pytest.mark.asyncio
async def test_remove_user(db: AsyncSession, client: TestClient):
    user_data = await generate_user(db, is_admin=True)
    auth_client(client, user_data.email, user_data.password)

    user = await db.get_one(User, user_data.id)

    resp = client.delete(f"/v1/users/{user.id}")
    assert resp.status_code == 204

    stmt = select(User).where(User.id == user_data.id).limit(1)
    user = await db.scalar(stmt)
    assert user is None


@pytest.mark.asyncio
async def test_not_admin_remove_user(db: AsyncSession, client: TestClient):
    user_data = await generate_user(db)
    auth_client(client, user_data.email, user_data.password)

    user = await db.get_one(User, user_data.id)

    resp = client.delete(f"/v1/users/{user.id}")
    assert resp.status_code == 403

    user = await db.get(User, user_data.id)
    assert user is not None
