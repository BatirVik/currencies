from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import sql
from sqlalchemy.exc import IntegrityError
from loguru import logger

from app.exceptions.user import EmailAlreadyTaken, UserNotFound, AuthenticationFailed
from app.schemes.user import UserCreate, UserResetPassword, UserUpdate
from app.models.user import User
from app.auth import hash_password, verify_password


async def create(
        db: AsyncSession, user_scheme: UserCreate, is_admin: bool = False
) -> User:
    user = User(
        **user_scheme.model_dump(exclude={"password"}),
        hashed_password=hash_password(user_scheme.password),
        is_admin=is_admin,
    )
    db.add(user)
    try:
        await db.commit()
    except IntegrityError as exc:
        logger.debug("Catched: {!r}", exc)
        await db.rollback()
        raise EmailAlreadyTaken(user.email)
    return user


async def read_by_email(db: AsyncSession, user_email: str) -> User:
    stmt = sql.select(User).where(User.email == user_email)
    if user := await db.scalar(stmt):
        return user
    raise UserNotFound(user_email)


async def read(db: AsyncSession, user_id: UUID) -> User:
    stmt = sql.select(User).where(User.id == user_id)
    if user := await db.scalar(stmt):
        return user
    raise UserNotFound(user_id)


async def delete(db: AsyncSession, user_id: UUID) -> None:
    stmt = sql.delete(User).where(User.id == user_id)
    res = await db.execute(stmt)
    await db.commit()
    if res.rowcount == 0:
        raise UserNotFound(user_id)


async def update(db: AsyncSession, user_id: UUID, user_scheme: UserUpdate) -> User:
    update_data = user_scheme.model_dump(exclude={"password"}, exclude_none=True)
    if user_scheme.password is not None:
        update_data["hashed_password"] = hash_password(user_scheme.password)
    stmt = (
        sql.update(User).where(User.id == user_id).values(**update_data).returning(User)
    )
    try:
        user = await db.scalar(stmt)
    except IntegrityError as exc:
        logger.debug("Catched: {!r}", exc)
        await db.rollback()
        raise EmailAlreadyTaken(user_scheme.email)

    if user is None:
        raise UserNotFound(user_id)

    await db.commit()
    return user


async def reset_password(db: AsyncSession, user: User, reset_scheme: UserResetPassword) -> None:
    if not verify_password(reset_scheme.old_password, user.hashed_password):
        raise AuthenticationFailed(user.id)
    user.hashed_password = hash_password(reset_scheme.new_password)
    await db.commit()
