from datetime import datetime
from uuid import uuid4

from typing import Annotated
from uuid import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import func

type uuidpk = Annotated[UUID, mapped_column(primary_key=True, default=uuid4)]


class Base(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )
