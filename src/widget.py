from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info: str) -> str:
    """Принимает строку с типом и номером карты/счета и возвращает её с замаскированным номером."""
    parts = info.split()
    num_index = -1

    for i, part in enumerate(parts):
        if part.isdigit():
            num_index = i
            break

    if num_index == -1:
        return info

    name = " ".join(parts[:num_index])
    number = parts[num_index]

    if name.lower().startswith("счет"):
        return f"{name} {get_mask_account(number)}"
    else:
        return f"{name} {get_mask_card_number(number)}"


def get_date(date_str: str) -> str:
    """Трансформирует строку с датой в формат ДД.ММ.ГГГГ"""
    date_part = date_str.split("T")[0]
    year, month, day = date_part.split("-")
    return f"{day}.{month}.{year}"
