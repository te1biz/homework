
from pathlib import Path
from typing import Any, cast

import pandas as pd


def read_csv_transactions(
    path: str | Path,
) -> list[dict[str, Any]]:
    """Считывает финансовые транзакции из CSV-файла."""
    dataframe = pd.read_csv(path)
    records = dataframe.to_dict(orient="records")
    return cast(list[dict[str, Any]], records)


def read_excel_transactions(
    path: str | Path,
) -> list[dict[str, Any]]:
    """Считывает финансовые транзакции из Excel-файла."""
    dataframe = pd.read_excel(path)
    records = dataframe.to_dict(orient="records")
    return cast(list[dict[str, Any]], records)
