import pytest
from decimal import Decimal
from app.schemes.currency import CurrenciesList, CurrencyScheme


@pytest.mark.parametrize("code", ["USD", "usD", "JUSD"])
def test_currency_code_validation(code: str):
    if len(code) == 3:
        curr = CurrencyScheme(code=code, equals_usd=Decimal(1))
        assert curr.code == code.upper()
        return

    with pytest.raises(ValueError):
        CurrencyScheme(code=code, equals_usd=Decimal(1))


@pytest.mark.parametrize(
    "codes",
    [
        ["USD", "UKR", "HRK"],
        ["UKR", "UKR", "HRK"],
    ],
)
def test_duplicate_currencies(codes: list[str]):
    currs_data = [CurrencyScheme(code=code, equals_usd=Decimal(1)) for code in codes]
    if len(set(codes)) == len(codes):
        CurrenciesList(currencies=currs_data)
        return

    with pytest.raises(ValueError):
        CurrenciesList(currencies=currs_data)
