import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.testclient import TestClient

from app import crud
from app.schemes.user import UserCreate


@pytest.mark.asyncio
async def test_get_token(db: AsyncSession, client: TestClient):
    user = await crud.user.create(
        db, UserCreate(email="user@gmail.com", password="123%0=Hello")
    )
    assert user is not None

    resp = client.post(
        "/v1/auth/token", data={"username": "user@gmail.com", "password": "123%0=Hello"}
    )
    assert resp.status_code == 200
    assert resp.json().keys() == {"access_token", "token_type"}


@pytest.mark.asyncio
async def test_get_token__invalid_password(db: AsyncSession, client: TestClient):
    user = await crud.user.create(
        db, UserCreate(email="user@gmail.com", password="123%0=Hello")
    )
    assert user is not None

    resp = client.post(
        "/v1/auth/token", data={"username": "user@gmail.com", "password": "12345678"}
    )
    assert resp.status_code == 401
