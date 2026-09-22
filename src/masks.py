def get_mask_card_number(card_number: int | str) -> str:
    """Принимает на вход номер карты и возвращает ее маску"""
    mask_card_number = (
        str(card_number)[0:4]
        + " "
        + str(card_number)[4:6]
        + " ****"
        + str(card_number)[-4:]
    )
    return mask_card_number


def get_mask_account(account_number: int | str) -> str:
    """принимает на вход номер счета и возвращает его маску"""
    mask_account_number = "" + str(account_number)[-4:]
    return mask_account_number