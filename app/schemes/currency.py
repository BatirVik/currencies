from decimal import Decimal
from pydantic import BaseModel, Field, field_validator


class CurrencyScheme(BaseModel):
    code: str = Field(min_length=3, max_length=3)
    equals_usd: Decimal

    @field_validator("code")
    def uppercase_code(cls, code: str) -> str:
        return code.upper()


class CurrencyRead(CurrencyScheme):
    pass


class CurrenciesList(BaseModel):
    currencies: list[CurrencyScheme]

    @field_validator("currencies")
    def validate_currencies(cls, currs: list[CurrencyScheme]) -> list[CurrencyScheme]:
        unique_codes = set(curr.code for curr in currs)
        if len(currs) != len(unique_codes):
            raise ValueError(
                "Currencies contains code duplicates, which is not allowed"
            )
        return currs


class CurrenciesRead(BaseModel):
    currencies: list[CurrencyRead]
