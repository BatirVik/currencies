from uuid import UUID

from fastapi import HTTPException
from fastapi.routing import APIRouter

from app.db import SessionDepends
from app.schemes.user import UserCreate, UserRead, UserResetPassword, UserUpdate
from app.models.user import User
from app import crud
from app.auth import UserDepends, admin_depends


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=201, response_model=UserRead)
async def register_user(db: SessionDepends, user_scheme: UserCreate) -> User:
    if user := await crud.user.create(db, user_scheme):
        return user
    raise HTTPException(409, "Email is already taken")


@router.post(
    "/admin", status_code=201, response_model=UserRead, dependencies=[admin_depends]
)
async def register_admin(db: SessionDepends, user_scheme: UserCreate) -> User:
    if user := await crud.user.create(db, user_scheme, is_admin=True):
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


@router.delete("/{user_id}", status_code=204, dependencies=[admin_depends])
async def remove_user_by_id(db: SessionDepends, user_id: UUID) -> None:
    is_deleted = await crud.user.delete(db, user_id)
    if not is_deleted:
        raise HTTPException(404, "User not found")


@router.patch("/{user_id}", dependencies=[admin_depends], response_model=UserRead)
async def update_user_by_id(
    db: SessionDepends, user_id: UUID, user_scheme: UserUpdate
) -> User:
    on_coflict = HTTPException(409, "Email is already taken")
    if user := await crud.user.update(db, user_id, user_scheme, on_coflict):
        return user
    raise HTTPException(404, "User not found")


@router.patch("/me/reset-password", status_code=204)
async def reset_password(
    db: SessionDepends, reset_scheme: UserResetPassword, user: UserDepends
) -> None:
    await crud.user.reset_password(
        db,
        user,
        reset_scheme,
        authentication_failed=HTTPException(400, "Authentication failed"),
    )
