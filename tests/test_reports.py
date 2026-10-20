import json
from pathlib import Path
from typing import Any

import pandas as pd
import pytest

from src.reports import report_saver, spending_by_category


def test_spending_by_category_filters_three_months_and_saves_report(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    transactions = pd.DataFrame(
        [
            {"date": "2024-01-29", "category": "Food", "amount": 10},
            {"date": "2024-01-30", "category": "Food", "amount": 20},
            {"date": "2024-02-15", "category": "Food", "amount": 30},
            {"date": "2024-04-30", "category": "food", "amount": 40},
            {"date": "2024-05-01", "category": "Food", "amount": 50},
            {"date": "2024-03-01", "category": "Travel", "amount": 60},
        ]
    )

    result = spending_by_category(transactions, "FOOD", "2024-04-30")

    assert result["amount"].tolist() == [20, 30, 40]
    saved = json.loads((tmp_path / "reports.json").read_text(encoding="utf-8"))
    assert [item["amount"] for item in saved] == [20, 30, 40]


def test_spending_by_category_supports_russian_column_names(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.chdir(tmp_path)
    transactions = pd.DataFrame(
        [
            {"Дата операции": "2024-01-15", "Категория": "Продукты", "Сумма платежа": -300},
            {"Дата операции": "2024-02-15", "Категория": "Переводы", "Сумма платежа": -500},
        ]
    )

    result = spending_by_category(transactions, "Продукты", "2024-03-31")

    assert result["Категория"].tolist() == ["Продукты"]
    assert result["Сумма платежа"].tolist() == [-300]


def test_report_saver_accepts_custom_filename(tmp_path: Path) -> None:
    destination = tmp_path / "custom" / "result.json"

    @report_saver(filename=destination)
    def report(value: int) -> dict[str, Any]:
        return {"total": value}

    assert report(42) == {"total": 42}
    assert json.loads(destination.read_text(encoding="utf-8")) == {"total": 42}


def test_spending_by_category_rejects_missing_columns() -> None:
    with pytest.raises(ValueError, match="дата"):
        spending_by_category(pd.DataFrame({"value": [1]}), "Food", "2024-03-31")


def test_spending_by_category_rejects_invalid_date() -> None:
    data = pd.DataFrame({"date": ["2024-01-01"], "category": ["Food"]})
    with pytest.raises(ValueError, match="YYYY-MM-DD"):
        spending_by_category(data, "Food", "not-a-date")
