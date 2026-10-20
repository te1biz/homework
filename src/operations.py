
from typing import Any


def process_bank_operations(
    data: list[dict[str, Any]],
    categories: list[str],
) -> dict[str, int]:
    """Подсчитывает количество транзакций в каждой категории."""
    result = {category: 0 for category in categories}

    for transaction in data:
        description = transaction.get("description", "")

        if description in result:
            result[description] += 1

    return result
