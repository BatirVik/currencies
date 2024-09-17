from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

from bcrypt import gensalt, hashpw, checkpw
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
from jwt.exceptions import InvalidTokenError
import jwt

from app.config import config
from app import crud
from app.models.user import User
from app.schemes.token import TokenData
from app.db import SessionDepends

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/token")


def hash_password(password: str) -> str:
    return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    return checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    if user := await crud.user.read_by_email(db, email):
        if verify_password(password, user.hashed_password):
            return user


def create_access_token(payload: dict[str, Any], expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {**payload, "exp": expire}
    return jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)


async def get_user(
    db: SessionDepends, token: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = await crud.user.read_by_email(db, token_data.email)
    if user is None:
        raise credentials_exception
    return user


async def get_admin(user: Annotated[User, Depends(get_user)]) -> User:
    if user.is_admin:
        return user
    raise HTTPException(403, "Forbidden")


user_depends = Depends(get_user)
admin_depends = Depends(get_admin)

UserDepends = Annotated[User, user_depends]
AdminDepends = Annotated[User, admin_depends]
