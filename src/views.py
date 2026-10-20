"""Формирование данных для страницы «Главная»."""

import json
import logging
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SETTINGS_PATH = PROJECT_ROOT / "user_settings.json"
EXCHANGE_RATES_URL = "https://api.apilayer.com/exchangerates_data/latest"
STOCK_PRICE_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"


def _value(transaction: dict[str, Any], *names: str, default: Any = "") -> Any:
    """Возвращает значение по первому найденному имени поля."""
    for name in names:
        if name in transaction:
            return transaction[name]
    return default


def _parse_date(value: Any) -> datetime | None:
    """Разбирает даты из форматов Excel задания и CSV проекта."""
    if isinstance(value, datetime):
        return value
    if value is None or value == "":
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        for date_format in ("%d.%m.%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(str(value), date_format)
            except ValueError:
                continue
    return None


def _load_settings(settings_path: str | Path) -> dict[str, list[str]]:
    """Читает пользовательские валюты и тикеры; при ошибке берёт пустые списки."""
    try:
        with Path(settings_path).open(encoding="utf-8") as settings_file:
            settings = json.load(settings_file)
        if not isinstance(settings, dict):
            raise ValueError("Настройки должны быть JSON-объектом")
        currencies = settings.get("user_currencies", [])
        stocks = settings.get("user_stocks", [])
        if not isinstance(currencies, list) or not isinstance(stocks, list):
            raise ValueError("user_currencies и user_stocks должны быть списками")
        return {
            "user_currencies": [str(item).upper() for item in currencies],
            "user_stocks": [str(item).upper() for item in stocks],
        }
    except (OSError, json.JSONDecodeError, ValueError) as error:
        logger.error("Не удалось загрузить настройки %s: %s", settings_path, error)
        return {"user_currencies": [], "user_stocks": []}


def _currency_rates(currencies: list[str]) -> list[dict[str, Any]]:
    """Получает курс одной единицы каждой валюты к рублю."""
    rates: list[dict[str, Any]] = []
    api_key = os.getenv("EXCHANGE_RATES_API_KEY")
    for currency in currencies:
        try:
            if currency == "RUB":
                rate = 1.0
            elif not api_key:
                raise ValueError("Не задан EXCHANGE_RATES_API_KEY")
            else:
                response = requests.get(
                    EXCHANGE_RATES_URL,
                    headers={"apikey": api_key},
                    params={"base": "RUB", "symbols": currency},
                    timeout=10,
                )
                response.raise_for_status()
                quote_per_ruble = float(response.json()["rates"][currency])
                if quote_per_ruble <= 0:
                    raise ValueError("API вернул неположительный курс")
                rate = 1.0 / quote_per_ruble
            rates.append({"currency": currency, "rate": float(rate)})
        except (requests.RequestException, KeyError, TypeError, ValueError) as error:
            logger.warning("Не удалось получить курс %s: %s", currency, error)
            rates.append({"currency": currency, "rate": 0.0, "error": str(error)})
    return rates


def _stock_prices(stocks: list[str]) -> list[dict[str, Any]]:
    """Получает последнюю доступную цену тикеров через Yahoo Finance chart API."""
    prices: list[dict[str, Any]] = []
    headers = {"User-Agent": "Mozilla/5.0"}
    for stock in stocks:
        try:
            response = requests.get(
                STOCK_PRICE_URL.format(symbol=stock),
                params={"range": "1d", "interval": "1d"},
                headers=headers,
                timeout=10,
            )
            response.raise_for_status()
            result = response.json()["chart"]["result"][0]
            quote = result["indicators"]["quote"][0]
            values = [value for value in quote.get("close", []) if value is not None]
            if not values and result.get("meta", {}).get("regularMarketPrice") is not None:
                values = [result["meta"]["regularMarketPrice"]]
            if not values:
                raise ValueError("API не вернул цену акции")
            price = float(values[-1])
            if price <= 0:
                raise ValueError("API вернул неположительную цену")
            prices.append({"stock": stock, "price": price})
        except (requests.RequestException, KeyError, IndexError, TypeError, ValueError) as error:
            logger.warning("Не удалось получить цену акции %s: %s", stock, error)
            prices.append({"stock": stock, "price": 0.0, "error": str(error)})
    return prices


def _greeting(hour: int) -> str:
    if 6 <= hour <= 11:
        return "Доброе утро"
    if 12 <= hour <= 17:
        return "Добрый день"
    if 18 <= hour <= 22:
        return "Добрый вечер"
    return "Доброй ночи"


def _card_summary(
    transactions: list[dict[str, Any]], start: datetime, end: datetime
) -> list[dict[str, Any]]:
    totals: dict[str, float] = defaultdict(float)
    for transaction in transactions:
        operation_date = _parse_date(_value(transaction, "Дата операции", "date"))
        state = str(_value(transaction, "Статус", "state", default="EXECUTED")).upper()
        if (
            operation_date is None
            or not start.date() <= operation_date.date() <= end.date()
        ):
            continue
        if state not in ("OK", "EXECUTED"):
            continue
        card_field = _value(transaction, "Номер карты", "from")
        digits = "".join(character for character in str(card_field) if character.isdigit())
        if not digits or "счет" in str(card_field).lower() or "счёт" in str(card_field).lower():
            continue
        amount = _value(transaction, "Сумма платежа", "amount", default=0)
        try:
            totals[digits[-4:]] += abs(float(amount))
        except (TypeError, ValueError):
            logger.warning(
                "Пропущена некорректная сумма транзакции %s", transaction.get("id")
            )
    return [
        {"last_digits": card, "total_spent": round(total, 2), "cashback": round(total // 100, 2)}
        for card, total in sorted(totals.items())
    ]


def _top_transactions(
    transactions: list[dict[str, Any]], start: datetime, end: datetime
) -> list[dict[str, Any]]:
    selected: list[tuple[float, dict[str, Any]]] = []
    for transaction in transactions:
        operation_date = _parse_date(_value(transaction, "Дата операции", "date"))
        state = str(_value(transaction, "Статус", "state", default="EXECUTED")).upper()
        if (
            operation_date is None
            or not start.date() <= operation_date.date() <= end.date()
        ):
            continue
        if state not in ("OK", "EXECUTED"):
            continue
        try:
            amount = float(_value(transaction, "Сумма платежа", "amount", default=0))
        except (TypeError, ValueError):
            continue
        selected.append((amount, transaction))

    top: list[dict[str, Any]] = []
    for amount, transaction in sorted(selected, key=lambda item: item[0], reverse=True)[:5]:
        operation_date = _parse_date(_value(transaction, "Дата операции", "date"))
        assert operation_date is not None
        top.append(
            {
                "date": operation_date.strftime("%d.%m.%Y"),
                "amount": amount,
                "category": str(_value(transaction, "Категория", "category", default="")),
                "description": str(_value(transaction, "Описание", "description", default="")),
            }
        )
    return top


def main_page(
    date_time: str,
    transactions: list[dict[str, Any]],
    settings_path: str | Path = DEFAULT_SETTINGS_PATH,
) -> str:
    """Формирует JSON главной страницы за начало месяца — указанную дату.

    Args:
        date_time: Дата и время в формате ``YYYY-MM-DD HH:MM:SS``.
        transactions: Транзакции, уже прочитанные из источника данных.
        settings_path: Путь к JSON-настройкам валют и акций.

    Returns:
        JSON-строку с приветствием, карточками, топ-5, курсами валют и ценами акций.
    """
    try:
        requested_at = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    except ValueError as error:
        raise ValueError("Дата должна быть в формате YYYY-MM-DD HH:MM:SS") from error

    start = requested_at.replace(day=1, hour=0, minute=0, second=0)
    settings = _load_settings(settings_path)
    result = {
        "greeting": _greeting(requested_at.hour),
        "cards": _card_summary(transactions, start, requested_at),
        "top_transactions": _top_transactions(transactions, start, requested_at),
        "currency_rates": _currency_rates(settings["user_currencies"]),
        "stock_prices": _stock_prices(settings["user_stocks"]),
    }
    return json.dumps(result, ensure_ascii=False)
