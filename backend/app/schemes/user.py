from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    is_admin: bool = False


class UserRead(BaseModel):
    id: UUID
    email: str
    is_admin: bool
