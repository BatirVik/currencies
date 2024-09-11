from decimal import Decimal
from typing_extensions import Literal
from pydantic import BaseModel, Field, field_validator


class Currency(BaseModel):
    code: str = Field(min_length=3, max_length=3)
    equals_usd: Decimal

    @field_validator('code')
    def uppercase_code(cls, code: str) -> str:
        return code.upper()


class Currencies(BaseModel):
    currencies: list[Currency]

    @field_validator('currencies')
    def validate_currencies(cls, currs: list[Currency]) -> list[Currency]:
        unique_codes = set(curr.code for curr in currs)
        if len(currs) != len(unique_codes):
            raise ValueError("Currencies contains code duplicates, which is not allowed")
        return currs


class CurrenciesRead(Currencies):
    pass


class CurrenciesUpdate(Currencies):
    on_absence: Literal["create", "skip", "abort"]


class CurrenciesCreate(Currencies):
    on_presence: Literal["update", "skip", "abort"]
