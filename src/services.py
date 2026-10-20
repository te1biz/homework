"""Сервисы для анализа банковских транзакций."""

import logging
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any

logger = logging.getLogger(__name__)
INVESTMENT_LIMITS = {10, 50, 100}


def _operation_date(value: Any) -> date | None:
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if value is None:
        return None
    text = str(value).strip()
    for date_format in ("%Y-%m-%d", "%Y-%m-%d %H:%M:%S", "%d.%m.%Y"):
        try:
            return datetime.strptime(text[:19], date_format).date()
        except ValueError:
            continue
    return None


def investment_bank(
    month: str,
    transactions: list[dict[str, Any]],
    limit: int,
) -> float:
    """Считает сумму, которую можно было отложить округлением трат.

    Для каждой положительной операции указанного месяца сумма округляется
    вверх до следующего шага `limit`, а разница добавляется к накоплениям.
    Поддерживаются форматы данных задания и русскоязычная выгрузка банка.
    """
    try:
        target_month = datetime.strptime(month, "%Y-%m").date()
    except ValueError as error:
        raise ValueError("Месяц должен быть в формате YYYY-MM") from error
    if target_month.strftime("%Y-%m") != month:
        raise ValueError("Месяц должен быть в формате YYYY-MM")
    if (
        isinstance(limit, bool)
        or not isinstance(limit, int)
        or limit not in INVESTMENT_LIMITS
    ):
        raise ValueError("Шаг округления должен быть одним из значений: 10, 50 или 100")

    savings = Decimal("0")
    step = Decimal(limit)
    for transaction in transactions:
        operation_date = _operation_date(
            transaction.get("Дата операции", transaction.get("date"))
        )
        if operation_date is None or operation_date.strftime("%Y-%m") != month:
            continue
        raw_amount = transaction.get("Сумма операции", transaction.get("amount"))
        try:
            amount = Decimal(str(raw_amount))
        except (InvalidOperation, TypeError):
            logger.warning("Пропущена некорректная сумма операции: %r", raw_amount)
            continue
        if not amount.is_finite() or amount <= 0:
            continue
        rounded_amount = (
            (amount / step).to_integral_value(rounding="ROUND_CEILING") * step
        )
        savings += rounded_amount - amount

    return float(savings)
