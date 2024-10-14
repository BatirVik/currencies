from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Numeric, CheckConstraint

from .base import Base


class Currency(Base):
    __tablename__ = "currency"

    code: Mapped[str] = mapped_column(primary_key=True)
    equals_usd: Mapped[Decimal] = mapped_column(Numeric(10, 4))

    __table_args__ = (
        CheckConstraint("LENGTH(code) = 3", name="check_code_lenght"),
        CheckConstraint("UPPER(code) = code", name="check_code_uppercase"),
        CheckConstraint("equals_usd > 0", name="check_equals_usd_positive"),
    )
