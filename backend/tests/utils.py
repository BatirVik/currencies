from typing import NamedTuple

from faker import Faker
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.testclient import TestClient

from app.models.user import User
from app.auth import hash_password


def auth_client(client: TestClient, email: str, password: str):
    resp = client.post(
        "v1/auth/token", data={"username": email, "password": password}
    ).raise_for_status()
    token = resp.json()["access_token"]
    client.headers["Authorization"] = f"Bearer {token}"


class LoginData(NamedTuple):
    email: str
    password: str


async def generate_login_data(db: AsyncSession, **kwargs) -> LoginData:
    email = Faker().email()
    password = "BestPasswordEver!123#"
    db.add(User(email=email, hashed_password=hash_password(password), **kwargs))
    await db.commit()
    return LoginData(email, password)
