import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.testclient import TestClient

from app import crud
from tests.utils import auth_client, generate_user


@pytest.mark.asyncio
async def test_get_user(db: AsyncSession, client: TestClient):
    user_data = await generate_user(db, is_admin=True)
    auth_client(client, user_data.email, user_data.password)

    user = await crud.user.read_one_by_email(db, user_data.email)

    resp = client.get(f"/v1/users/{user.id}")
    assert resp.status_code == 200

    assert resp.json() == {
        "id": str(user.id),
        "email": user_data.email,
        "is_admin": user.is_admin,
    }


@pytest.mark.asyncio
async def test_not_admin_get_user(db: AsyncSession, client: TestClient):
    user_data = await generate_user(db)
    auth_client(client, user_data.email, user_data.password)

    user = await crud.user.read_one_by_email(db, user_data.email)

    resp = client.get(f"/v1/users/{user.id}")
    assert resp.status_code == 403
