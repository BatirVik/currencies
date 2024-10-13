from uuid import UUID

from fastapi import HTTPException
from fastapi.routing import APIRouter

from app.db import SessionDepends
from app.exceptions.user import EmailAlreadyTaken, UserNotFound, AuthenticationFailed
from app.schemes.user import UserCreate, UserRead, UserResetPassword, UserUpdate
from app.models.user import User
from app import crud
from app.auth import UserDepends, admin_depends

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    status_code=201,
    response_model=UserRead,
    responses={
        409: {"description": "Email Already Taken"}
    }
)
async def register_user(db: SessionDepends, user_scheme: UserCreate) -> User:
    try:
        return await crud.user.create(db, user_scheme)
    except EmailAlreadyTaken:
        raise HTTPException(409, "Email is already taken")


@router.post(
    "/admin",
    status_code=201,
    response_model=UserRead,
    dependencies=[admin_depends],
    responses={
        409: {"description": "Email Already Taken"}
    }
)
async def register_admin(db: SessionDepends, user_scheme: UserCreate) -> User:
    try:
        return await crud.user.create(db, user_scheme, is_admin=True)
    except EmailAlreadyTaken:
        raise HTTPException(409, "Email is already taken")


@router.get("/me", response_model=UserRead)
async def get_current_user(user: UserDepends) -> User:
    return user


@router.get(
    "/{user_id}",
    response_model=UserRead,
    dependencies=[admin_depends],
    responses={
        404: {"description": "Not found"}
    }
)
async def get_user_by_id(db: SessionDepends, user_id: UUID) -> User:
    try:
        return await crud.user.read(db, user_id)
    except UserNotFound:
        raise HTTPException(404, "User not found")


@router.delete(
    "/{user_id}",
    status_code=204,
    dependencies=[admin_depends],
    responses={
        404: {"description": "Not found"}
    }
)
async def remove_user_by_id(db: SessionDepends, user_id: UUID) -> None:
    try:
        await crud.user.delete(db, user_id)
    except UserNotFound:
        raise HTTPException(404, "User not found")


@router.patch(
    "/{user_id}",
    dependencies=[admin_depends],
    response_model=UserRead,
    responses={
        404: {"description": "Not found"},
        409: {"description": "Email Already Taken"}
    }
)
async def update_user_by_id(
        db: SessionDepends, user_id: UUID, user_scheme: UserUpdate
) -> User:
    try:
        return await crud.user.update(db, user_id, user_scheme)
    except UserNotFound:
        raise HTTPException(404, "User not found")
    except EmailAlreadyTaken:
        raise HTTPException(409, "Email is already taken")


@router.patch(
    "/me/reset-password",
    status_code=204,
    responses={
        400: {"description": "Authentication Failed"},
    }
)
async def reset_password(
        db: SessionDepends, reset_scheme: UserResetPassword, user: UserDepends
) -> None:
    try:
        await crud.user.reset_password(db, user, reset_scheme)
    except AuthenticationFailed:
        raise HTTPException(400, "Authentication failed")
