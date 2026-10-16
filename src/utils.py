
import json
from pathlib import Path
from typing import Any


def load_transactions(file_path: str | Path) -> list[dict[str, Any]]:
    """Загружает список транзакций из JSON-файла."""
    try:
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return []

    if not isinstance(data, list):
        return []

    return [item for item in data if isinstance(item, dict)]
