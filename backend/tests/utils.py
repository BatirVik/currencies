from faker import Faker
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.testclient import TestClient

from app.schemes.user import UserCreate

from app import crud
from app.models.currency import Currency


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


async def create_currencies(db: AsyncSession, **kwargs: float) -> list[Currency]:
    currs = []
    for code, equals_usd in kwargs.items():
        if len(code) != 3:
            ValueError("All kwargs keys must have lenght 3")
        currs.append(Currency(code=code, equals_usd=equals_usd))
    db.add_all(currs)
    await db.commit()
    return currs
