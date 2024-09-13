from faker import Faker
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.testclient import TestClient

from app.schemes.user import UserCreate

from app import crud


def auth_client(client: TestClient, email: str, password: str):
    resp = client.post(
        "v1/auth/token", data={"username": email, "password": password}
    ).raise_for_status()
    token = resp.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"


async def generate_user(db: AsyncSession, **kwargs) -> UserCreate:
    user_scheme = UserCreate(
        email=generate_email(),
        password="BestPasswordEver!123#",
        **kwargs,
    )
    await crud.user.create(db, user_scheme)
    return user_scheme


def generate_email() -> str:
    return Faker().email()
