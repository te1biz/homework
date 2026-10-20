from datetime import datetime
from typing import Any


def filter_by_state(
    dict_list: list[dict[str, Any]],
    state: str = "EXECUTED",
) -> list[dict[str, Any]]:
    """Фильтрует транзакции по статусу."""
    normalized_state = state.upper()

    return [
        item
        for item in dict_list
        if item.get("state", "").upper() == normalized_state
    ]


def sort_by_date(
    dict_list: list[dict[str, Any]],
    is_reversed: bool = True,
) -> list[dict[str, Any]]:
    """Сортирует транзакции по дате."""
    return sorted(
        dict_list,
        key=lambda item: datetime.fromisoformat(item["date"]),
        reverse=is_reversed,
    )