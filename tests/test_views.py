import json
from pathlib import Path
from typing import Any
from unittest.mock import Mock

import pytest
import requests

from src.views import _greeting, main_page


@pytest.mark.parametrize(
    ("hour", "expected"),
    [
        (0, "Доброй ночи"),
        (5, "Доброй ночи"),
        (6, "Доброе утро"),
        (11, "Доброе утро"),
        (12, "Добрый день"),
        (17, "Добрый день"),
        (18, "Добрый вечер"),
        (22, "Добрый вечер"),
        (23, "Доброй ночи"),
    ],
)
def test_greeting(hour: int, expected: str) -> None:
    assert _greeting(hour) == expected


def test_main_page_builds_expected_json(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = tmp_path / "user_settings.json"
    settings.write_text(
        json.dumps({"user_currencies": ["USD"], "user_stocks": ["AAPL"]}),
        encoding="utf-8",
    )
    transactions: list[dict[str, Any]] = [
        {
            "date": f"2024-03-{day:02d}",
            "state": "EXECUTED",
            "from": "Visa 1234567812341111",
            "amount": amount,
            "category": "Покупки",
            "description": f"Покупка {day}",
        }
        for day, amount in ((1, 150), (2, 90), (3, 500), (4, 300), (5, 200), (6, 100))
    ]
    transactions.extend(
        [
            {
                "date": "2024-02-29",
                "state": "EXECUTED",
                "from": "Visa 1234567812341111",
                "amount": 9999,
                "category": "Покупки",
                "description": "До начала месяца",
            },
            {
                "date": "2024-03-07",
                "state": "CANCELED",
                "from": "Visa 1234567812341111",
                "amount": 9999,
                "category": "Покупки",
                "description": "Отменено",
            },
        ]
    )

    def fake_get(url: str, **kwargs: Any) -> Mock:
        response = Mock()
        response.raise_for_status.return_value = None
        if "exchangerates_data" in url:
            response.json.return_value = {"rates": {"USD": 0.01}}
        else:
            response.json.return_value = {
                "chart": {
                    "result": [
                        {
                            "indicators": {"quote": [{"close": [180.25]}]},
                            "meta": {},
                        }
                    ]
                }
            }
        return response

    monkeypatch.setenv("EXCHANGE_RATES_API_KEY", "test-key")
    monkeypatch.setattr("src.views.requests.get", fake_get)

    result = json.loads(main_page("2024-03-31 12:00:00", transactions, settings))

    assert result["greeting"] == "Добрый день"
    assert result["cards"] == [{"last_digits": "1111", "total_spent": 1340.0, "cashback": 13.0}]
    assert len(result["top_transactions"]) == 5
    assert [item["amount"] for item in result["top_transactions"]] == [500, 300, 200, 150, 100]
    assert all(set(item) == {"date", "amount", "category", "description"} for item in result["top_transactions"])
    assert result["currency_rates"] == [{"currency": "USD", "rate": 100.0}]
    assert result["stock_prices"] == [{"stock": "AAPL", "price": 180.25}]


def test_main_page_keeps_api_items_when_requests_fail(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = tmp_path / "user_settings.json"
    settings.write_text(
        json.dumps({"user_currencies": ["USD"], "user_stocks": ["AAPL"]}),
        encoding="utf-8",
    )
    monkeypatch.delenv("EXCHANGE_RATES_API_KEY", raising=False)
    monkeypatch.setattr(
        "src.views.requests.get",
        Mock(side_effect=requests.ConnectionError("offline")),
    )

    result = json.loads(main_page("2024-03-31 23:00:00", [], settings))

    assert result["greeting"] == "Доброй ночи"
    assert result["currency_rates"][0]["currency"] == "USD"
    assert result["currency_rates"][0]["rate"] == 0.0
    assert result["currency_rates"][0]["error"]
    assert result["stock_prices"][0]["stock"] == "AAPL"
    assert result["stock_prices"][0]["price"] == 0.0
    assert result["stock_prices"][0]["error"]


def test_main_page_rejects_wrong_datetime_format() -> None:
    with pytest.raises(ValueError, match="YYYY-MM-DD HH:MM:SS"):
        main_page("31.03.2024", [])
