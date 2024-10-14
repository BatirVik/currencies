from typing import Annotated
from datetime import timedelta

from fastapi import Depends, HTTPException
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from app.auth import authenticate_user
from app.db import SessionDepends
from app.auth import create_access_token
from app.config import config
from app.schemes.token import Token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/token",
    responses={401: {"description": "Unauthorized"}}
)
async def login(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: SessionDepends
) -> Token:
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token({"sub": user.email}, access_token_expires)
    return Token(access_token=access_token, token_type="bearer")
