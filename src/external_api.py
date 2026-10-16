
import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")
API_URL = "https://api.apilayer.com/exchangerates_data/convert"


def convert_to_rub(transaction: dict[str, Any]) -> float:
    """Возвращает сумму транзакции в рублях."""
    operation_amount = transaction.get("operationAmount", {})
    amount = float(operation_amount.get("amount", 0))
    currency = operation_amount.get("currency", {}).get("code", "RUB")

    if currency == "RUB":
        return amount

    if currency not in ("USD", "EUR"):
        raise ValueError(f"Неподдерживаемая валюта: {currency}")

    if not API_KEY:
        raise ValueError("Не задан EXCHANGE_RATES_API_KEY в файле .env")

    response = requests.get(
        API_URL,
        headers={"apikey": API_KEY},
        params={
            "from": currency,
            "to": "RUB",
            "amount": amount,
        },
        timeout=10,
    )
    response.raise_for_status()

    data = response.json()
    return float(data["result"])
