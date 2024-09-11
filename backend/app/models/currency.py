from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Currency(Base):
    __tablename__ = "currency"

    code: Mapped[str] = mapped_column(primary_key=True)
    equals_usd: Mapped[Decimal]
