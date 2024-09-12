from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import sql
from sqlalchemy.exc import IntegrityError

from app.schemes.user import UserCreate
from app.models.user import User
from app.auth import hash_password


async def create(db: AsyncSession, user_scheme: UserCreate) -> User | None:
    user = User(
        **user_scheme.model_dump(exclude={"password"}),
        hashed_password=hash_password(user_scheme.password),
    )
    db.add(user)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        return
    return user


async def read_by_email(db: AsyncSession, user_email: str) -> User | None:
    stmt = sql.select(User).where(User.email == user_email)
    return await db.scalar(stmt)
