"""Отчёты по банковским транзакциям."""

import json
import logging
from calendar import monthrange
from datetime import date, datetime
from functools import wraps
from pathlib import Path
from typing import Any, Callable, ParamSpec, TypeVar, cast

import pandas as pd

logger = logging.getLogger(__name__)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
P = ParamSpec("P")
R = TypeVar("R")


def report_saver(
    function: Callable[P, R] | str | Path | None = None,
    *,
    filename: str | Path | None = None,
) -> Any:
    """Декоратор сохранения результата отчёта в JSON.

    Использование: @report_saver, @report_saver() или
    @report_saver("reports/custom.json").
    """
    target = filename
    report_function: Callable[P, R] | None

    if callable(function):
        report_function = function
    else:
        report_function = None
        if function is not None:
            if target is not None:
                raise TypeError("Имя файла передано дважды")
            target = function

    # Для заданного имени путь фиксированный.
    # Путь по умолчанию определяется при вызове отчёта.
    destination = Path(target) if target is not None else None

    def decorate(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
            result = func(*args, **kwargs)
            report_path = destination or Path.cwd() / "reports.json"
            report_path.parent.mkdir(parents=True, exist_ok=True)

            if isinstance(result, pd.DataFrame):
                payload: Any = result.to_dict(orient="records")
            elif isinstance(result, pd.Series):
                payload = result.to_dict()
            else:
                payload = result

            try:
                with report_path.open("w", encoding="utf-8") as report_file:
                    json.dump(
                        payload,
                        report_file,
                        ensure_ascii=False,
                        indent=2,
                        default=str,
                    )
            except (OSError, TypeError, ValueError) as error:
                logger.exception(
                    "Не удалось сохранить отчёт в %s",
                    report_path,
                )
                raise OSError(
                    f"Не удалось сохранить отчёт в {report_path}"
                ) from error

            return result

        return wrapped

    if report_function is not None:
        return cast(Callable[P, R], decorate(report_function))
    return decorate

    def decorate(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
            result = func(*args, **kwargs)
            report_path = destination or Path.cwd() / "reports.json"
            report_path.parent.mkdir(parents=True, exist_ok=True)
            if isinstance(result, pd.DataFrame):
                payload: Any = result.to_dict(orient="records")
            elif isinstance(result, pd.Series):
                payload = result.to_dict()
            else:
                payload = result
            try:
                with report_path.open("w", encoding="utf-8") as report_file:
                    json.dump(payload, report_file, ensure_ascii=False, indent=2, default=str)
            except (OSError, TypeError, ValueError) as error:
                logger.exception("Не удалось сохранить отчёт в %s", report_path)
                raise OSError(f"Не удалось сохранить отчёт в {report_path}") from error
            return result

        return wrapped

    if report_function is not None:
        return cast(Callable[P, R], decorate(report_function))
    return decorate


def _subtract_three_months(value: date) -> date:
    month_index = value.year * 12 + value.month - 1 - 3
    year, month_zero_based = divmod(month_index, 12)
    month = month_zero_based + 1
    day = min(value.day, monthrange(year, month)[1])
    return date(year, month, day)


@report_saver
def spending_by_category(
    transactions: pd.DataFrame,
    category: str,
    date_to: str | date | datetime | None = None,
) -> pd.DataFrame:
    """Возвращает операции указанной категории за три месяца до даты включительно.

    Если `date_to` не задана, используется текущая дата.
    Поддерживаются колонки на русском языке из выгрузки банка и английские
    имена `date`, `category`, `amount` из учебного CSV.
    """
    if not isinstance(transactions, pd.DataFrame):
        raise TypeError("transactions должен быть pandas.DataFrame")

    if date_to is None:
        end_date = date.today()
    elif isinstance(date_to, datetime):
        end_date = date_to.date()
    elif isinstance(date_to, date):
        end_date = date_to
    else:
        try:
            end_date = datetime.fromisoformat(str(date_to)).date()
        except ValueError as error:
            raise ValueError("Дата должна быть ISO-датой YYYY-MM-DD") from error

    date_column = "Дата операции" if "Дата операции" in transactions.columns else "date"
    category_column = "Категория" if "Категория" in transactions.columns else "category"
    missing = [
        label
        for label, column in (("дата", date_column), ("категория", category_column))
        if column not in transactions.columns
    ]
    if missing:
        raise ValueError(f"В таблице отсутствуют обязательные колонки: {', '.join(missing)}")

    dates = pd.to_datetime(
        transactions[date_column], errors="coerce", utc=True
    ).dt.tz_convert(None)
    start_date = _subtract_three_months(end_date)
    mask = (
        transactions[category_column].astype(str).str.casefold().eq(category.casefold())
        & dates.ge(pd.Timestamp(start_date))
        & dates.lt(pd.Timestamp(end_date) + pd.Timedelta(days=1))
    )
    result = transactions.loc[mask].copy()
    logger.info(
        "Отчёт по категории %s: период %s — %s, найдено %d операций",
        category,
        start_date,
        end_date,
        len(result),
    )
    return result

