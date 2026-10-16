
from typing import Any

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


def test_filter_by_currency(
    transactions: list[dict[str, Any]],
) -> None:
    result = list(filter_by_currency(transactions, "USD"))
    actual_ids = [transaction["id"] for transaction in result]

    expected_ids = [
        939719570,
        142264268,
        895315941,
        123456789,
        987654321,
    ]

    assert actual_ids == expected_ids


def test_filter_by_currency_not_match(
    transactions: list[dict[str, Any]],
) -> None:
    result = list(filter_by_currency(transactions, "GBP"))

    assert result == []


def test_filter_by_currency_empty() -> None:
    result = list(filter_by_currency([], "USD"))

    assert result == []


def test_transaction_descriptions(
    transactions: list[dict[str, Any]],
) -> None:
    actual = list(transaction_descriptions(transactions))

    expected = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]

    assert actual == expected


def test_transaction_descriptions_empty() -> None:
    result = list(transaction_descriptions([]))

    assert result == []


def test_card_number_generator() -> None:
    result = list(card_number_generator(1, 3))

    assert result == [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
    ]


@pytest.mark.parametrize(
    ("start", "stop", "expected"),
    [
        (0, 0, ["0000 0000 0000 0000"]),
        (10, 10, ["0000 0000 0000 0010"]),
        (5, 3, []),
    ],
)
def test_card_number_generator_limits(
    start: int,
    stop: int,
    expected: list[str],
) -> None:
    assert list(card_number_generator(start, stop)) == expected
