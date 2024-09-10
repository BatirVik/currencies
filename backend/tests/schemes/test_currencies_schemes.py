import pytest
from decimal import Decimal
from app.schemes import Currency, Currencies


@pytest.mark.parametrize("code", ["USD", "usD", "JUSD"])
def test_currency_code_validation(code: str):
    if len(code) == 3:
        curr = Currency(code=code, equals_usd=Decimal(1))
        assert curr.code == code.upper()
        return

    with pytest.raises(ValueError):
        Currency(code=code, equals_usd=Decimal(1))


@pytest.mark.parametrize(
    "codes",
    [
        ["USD", "UKR", "HRK"],
        ["UKR", "UKR", "HRK"],
    ],
)
def test_duplicate_currencies(codes: list[str]):
    currs_data = [Currency(code=code, equals_usd=Decimal(1)) for code in codes]
    if len(set(codes)) == len(codes):
        Currencies(currencies=currs_data)
        return

    with pytest.raises(ValueError):
        Currencies(currencies=currs_data)
