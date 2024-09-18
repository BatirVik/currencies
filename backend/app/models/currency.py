from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Numeric

from .base import Base


class Currency(Base):
    __tablename__ = "currency"

    code: Mapped[str] = mapped_column(primary_key=True)
    equals_usd: Mapped[Decimal] = mapped_column(Numeric(10, 4))
