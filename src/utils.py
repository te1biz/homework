import json
from pathlib import Path
from typing import Any
import logging


LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    file_handler = logging.FileHandler(
        LOG_DIR / "utils.log",
        mode="w",
        encoding="utf-8",
    )
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.propagate = False


def load_transactions(file_path: str | Path) -> list[dict[str, Any]]:
    """Загружает список транзакций из JSON-файла."""
    logger.info("Loading transactions from %s", file_path)

    try:
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError, OSError) as error:
        logger.error("Failed to load transactions: %s", error)
        return []

    if not isinstance(data, list):
        logger.warning("JSON file does not contain a list")
        return []

    transactions = [item for item in data if isinstance(item, dict)]
    logger.info("Loaded %d transactions", len(transactions))
    return transactions
