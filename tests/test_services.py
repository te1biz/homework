from typing import Any

import pytest

from src.services import investment_bank


def test_investment_bank_sums_rounding_for_requested_month() -> None:
    transactions: list[dict[str, Any]] = [
        {"Дата операции": "2024-03-01", "Сумма операции": 1712},
        {"Дата операции": "2024-03-15", "Сумма операции": 1750},
        {"Дата операции": "2024-02-29", "Сумма операции": 129},
        {"Дата операции": "2024-03-20", "Сумма операции": -100},
    ]

    assert investment_bank("2024-03", transactions, 50) == 38.0


@pytest.mark.parametrize(
    ("amount", "limit", "expected"),
    [(1712, 10, 8.0), (1712, 50, 38.0), (1712, 100, 88.0), (1700, 50, 0.0)],
)
def test_investment_bank_rounds_up_to_step(amount: int, limit: int, expected: float) -> None:
    transactions = [{"date": "2024-03-01", "amount": amount}]
    assert investment_bank("2024-03", transactions, limit) == expected


def test_investment_bank_returns_zero_for_empty_month() -> None:
    transactions = [{"date": "2024-02-29", "amount": 1712}]
    assert investment_bank("2024-03", transactions, 50) == 0.0


@pytest.mark.parametrize("month", ["2024-3", "2024-13", "bad"])
def test_investment_bank_rejects_invalid_month(month: str) -> None:
    with pytest.raises(ValueError, match="YYYY-MM"):
        investment_bank(month, [], 50)


@pytest.mark.parametrize("limit", [0, 5, 25, 101, True])
def test_investment_bank_rejects_unsupported_limit(limit: int) -> None:
    with pytest.raises(ValueError, match="10, 50 или 100"):
        investment_bank("2024-03", [], limit)
