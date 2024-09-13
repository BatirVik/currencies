from decimal import Decimal
from datetime import datetime

from typing import Annotated
from uuid import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import CheckConstraint, func

type uuidpk = Annotated[UUID, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuidpk]
    email: Mapped[str]
    hashed_password: Mapped[str]


class Currency(Base):
    __tablename__ = "currency"

    code: Mapped[str] = mapped_column(unique=True)
    equals_usd: Mapped[Decimal]

    __table_args__ = (
        CheckConstraint("LEN(code) = 3", name="check_code_lenght"),
        CheckConstraint("UPPER(code) = code", name="check_code_uppercase"),
        CheckConstraint("equals_usd > 0", name="check_equals_usd_positive"),
    )
