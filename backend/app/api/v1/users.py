from uuid import UUID

from fastapi import HTTPException
from fastapi.routing import APIRouter

from app.db import SessionDepends
from app.schemes.user import UserCreate, UserRead
from app.models.user import User
from app import crud
from app.auth import admin_depends, UserDepends


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=201, response_model=UserRead)
async def register_user(db: SessionDepends, user_scheme: UserCreate) -> User:
    if user := await crud.user.create(db, user_scheme):
        return user
    raise HTTPException(409, "Email is already taken")


@router.get("/me", response_model=UserRead)
async def get_current_user(db: SessionDepends, user: UserDepends) -> User:
    return user


@router.get("/{user_id}", response_model=UserRead, dependencies=[admin_depends])
async def get_user_by_id(db: SessionDepends, user_id: UUID) -> User:
    if user := await crud.user.read(db, user_id):
        return user
    raise HTTPException(404, "User not found")
