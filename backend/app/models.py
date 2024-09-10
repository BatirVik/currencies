from decimal import Decimal
from datetime import datetime


from typing import Annotated
from uuid import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import func

type uuidpk = Annotated[UUID, mapped_column(primary_key=True)]


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )


class Account(Base):
    id: Mapped[uuidpk]
    email: Mapped[str]
    hashed_password: Mapped[str]


class Currency(Base):
    code: Mapped[str] = mapped_column(primary_key=True)
    equals_usd: Mapped[Decimal]
