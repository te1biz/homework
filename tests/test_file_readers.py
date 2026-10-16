
from unittest.mock import Mock, patch

import pandas as pd

from src.file_readers import read_csv_transactions, read_excel_transactions


@patch("src.file_readers.pd.read_csv")
def test_read_csv_transactions(mock_read_csv: Mock) -> None:
    """Проверяет чтение транзакций из CSV."""
    expected = [
        {"id": 1, "amount": 100},
        {"id": 2, "amount": 200},
    ]
    mock_read_csv.return_value = pd.DataFrame(expected)

    result = read_csv_transactions("transactions.csv")

    mock_read_csv.assert_called_once_with("transactions.csv")
    assert result == expected


@patch("src.file_readers.pd.read_excel")
def test_read_excel_transactions(mock_read_excel: Mock) -> None:
    """Проверяет чтение транзакций из Excel."""
    expected = [
        {"id": 1, "amount": 100},
        {"id": 2, "amount": 200},
    ]
    mock_read_excel.return_value = pd.DataFrame(expected)

    result = read_excel_transactions("transactions.xlsx")

    mock_read_excel.assert_called_once_with("transactions.xlsx")
    assert result == expected
