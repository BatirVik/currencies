from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import sql
from sqlalchemy.exc import IntegrityError

from app.schemes.user import UserCreate, UserResetPassword, UserUpdate
from app.models.user import User
from app.auth import hash_password, verify_password


async def create(
    db: AsyncSession, user_scheme: UserCreate, is_admin: bool = False
) -> User | None:
    user = User(
        **user_scheme.model_dump(exclude={"password"}),
        hashed_password=hash_password(user_scheme.password),
        is_admin=is_admin,
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


async def read(db: AsyncSession, user_id: UUID) -> User | None:
    return await db.get(User, user_id)


async def delete(db: AsyncSession, user_id: UUID) -> bool:
    stmt = sql.delete(User).where(User.id == user_id)
    res = await db.execute(stmt)
    await db.commit()
    return bool(res.rowcount)


async def update(
    db: AsyncSession,
    user_id: UUID,
    user_scheme: UserUpdate,
    on_conflict: Exception | None = None,
) -> User | None:
    update_data = user_scheme.model_dump(exclude={"password"}, exclude_none=True)
    if user_scheme.password is not None:
        update_data["hashed_password"] = hash_password(user_scheme.password)
    stmt = (
        sql.update(User).where(User.id == user_id).values(**update_data).returning(User)
    )
    try:
        user = await db.scalar(stmt)
    except IntegrityError as exc:
        await db.rollback()
        if on_conflict is None:
            raise exc
        raise on_conflict
    await db.commit()
    return user


async def read_one_by_email(db: AsyncSession, user_email: str) -> User:
    stmt = sql.select(User).where(User.email == user_email)
    res = await db.execute(stmt)
    return res.scalar_one()


async def reset_password(
    db: AsyncSession,
    user: User,
    reset_scheme: UserResetPassword,
    *,
    authentication_failed: Exception | None = None,
) -> bool:
    if not verify_password(reset_scheme.old_password, user.hashed_password):
        if authentication_failed is None:
            return False
        raise authentication_failed
    user.hashed_password = hash_password(reset_scheme.new_password)
    await db.commit()
    return True
