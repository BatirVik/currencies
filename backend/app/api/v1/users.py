from fastapi import HTTPException
from fastapi.routing import APIRouter

from app.db import SessionDepends
from app.schemes.user import UserCreate, UserRead
from app.models.user import User
from app import crud
from app.auth import UserDepends


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=201, response_model=UserRead)
async def register_user(db: SessionDepends, user_scheme: UserCreate) -> User:
    if user := await crud.user.create(db, user_scheme):
        return user
    raise HTTPException(409, "Email is already taken")


@router.get("/me", status_code=201, response_model=UserRead)
async def get_current_user(db: SessionDepends, user: UserDepends) -> User:
    return user
