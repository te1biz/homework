
import json
from typing import Any

import pytest

from src.utils import load_transactions


def test_load_transactions(tmp_path: Any) -> None:
    file_path = tmp_path / "operations.json"
    transactions = [
        {"id": 1, "amount": "1000"},
        {"id": 2, "amount": "2000"},
    ]
    file_path.write_text(
        json.dumps(transactions),
        encoding="utf-8",
    )

    assert load_transactions(file_path) == transactions


def test_load_empty_file(tmp_path: Any) -> None:
    file_path = tmp_path / "empty.json"
    file_path.write_text("", encoding="utf-8")

    assert load_transactions(file_path) == []


def test_load_missing_file(tmp_path: Any) -> None:
    file_path = tmp_path / "missing.json"

    assert load_transactions(file_path) == []


@pytest.mark.parametrize(
    "content",
    ['{"id": 1}', '"text"', "123", "null"],
)
def test_load_not_a_list(tmp_path: Any, content: str) -> None:
    file_path = tmp_path / "invalid_structure.json"
    file_path.write_text(content, encoding="utf-8")

    assert load_transactions(file_path) == []


def test_load_invalid_json(tmp_path: Any) -> None:
    file_path = tmp_path / "broken.json"
    file_path.write_text("{invalid json", encoding="utf-8")

    assert load_transactions(file_path) == []
