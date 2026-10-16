
from typing import Any

import pytest


@pytest.fixture
def transactions() -> list[dict[str, Any]]:
    """Тестовые транзакции для проверки генераторов."""
    return [
        {
            "id": 939719570,
            "description": "Перевод организации",
            "operationAmount": {
                "amount": "1000.00",
                "currency": {"name": "Доллар США", "code": "USD"},
            },
        },
        {
            "id": 142264268,
            "description": "Перевод со счета на счет",
            "operationAmount": {
                "amount": "200.00",
                "currency": {"name": "Доллар США", "code": "USD"},
            },
        },
        {
            "id": 895315941,
            "description": "Перевод со счета на счет",
            "operationAmount": {
                "amount": "500.00",
                "currency": {"name": "Доллар США", "code": "USD"},
            },
        },
        {
            "id": 123456789,
            "description": "Перевод с карты на карту",
            "operationAmount": {
                "amount": "300.00",
                "currency": {"name": "Доллар США", "code": "USD"},
            },
        },
        {
            "id": 987654321,
            "description": "Перевод организации",
            "operationAmount": {
                "amount": "750.00",
                "currency": {"name": "Доллар США", "code": "USD"},
            },
        },
    ]
