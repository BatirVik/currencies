from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, uuidpk


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuidpk]
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    is_admin: Mapped[bool]
