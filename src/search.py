
import re
from typing import Any


def process_bank_search(
    data: list[dict[str, Any]],
    search: str,
) -> list[dict[str, Any]]:
    """Ищет операции по тексту в поле description."""
    pattern = re.compile(re.escape(search), re.IGNORECASE)

    return [
        transaction
        for transaction in data
        if pattern.search(str(transaction.get("description", "")))
    ]
