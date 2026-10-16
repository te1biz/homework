
import logging
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler(
        LOG_DIR / "masks.log",
        mode="w",
        encoding="utf-8",
    )
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    logger.propagate = False


def get_mask_card_number(user_card_number: str) -> str:
    """Маскирует номер карты пользователя."""
    logger.info("Masking card number")

    if not user_card_number.strip():
        logger.error("Card number must not be empty")
        raise ValueError("Номер карты не должен быть пустым")

    result = (
        f"{user_card_number[:4]} "
        f"{user_card_number[4:6]}** **** "
        f"{user_card_number[-4:]}"
    )
    logger.info("Card number masked successfully")
    return result


def get_mask_account(user_account_number: str) -> str:
    """Маскирует номер счёта, оставляя последние четыре символа."""
    logger.info("Masking account number")
    account_number = user_account_number.strip()

    if len(account_number) < 4:
        logger.error("Account number must contain at least 4 characters")
        raise ValueError(
            "Номер счёта должен содержать не менее 4 символов"
        )

    result = "**" + account_number[-4:]
    logger.info("Account number masked successfully")
    return result
