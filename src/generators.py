
from collections.abc import Iterator
from typing import Any


def filter_by_currency(
    transactions: list[dict[str, Any]],
    currency: str,
) -> Iterator[dict[str, Any]]:
    """Возвращает транзакции с указанным кодом валюты."""
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction


def transaction_descriptions(
    transactions: list[dict[str, Any]],
) -> Iterator[str]:
    """Возвращает описания всех транзакций."""
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """Генерирует номера карт в заданном диапазоне."""
    for number in range(start, stop + 1):
        digits = f"{number:016d}"
        yield f"{digits[:4]} {digits[4:8]} {digits[8:12]} {digits[12:16]}"
