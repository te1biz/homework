from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(info_string: str) -> str:
    """Принимает на вход строку с типом и исходным номером карты или счета,
    определяет тип платежного средства и возвращает строку с замаскированным
    номером.
    """
    parts = info_string.split()
    number = parts[-1]
    name = " ".join(parts[:-1])

    if name.lower() == "счет":
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}"
