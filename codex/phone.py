"""Нормализация российских телефонных номеров."""


def normalize_phone(value):
    """Возвращает номер в формате +7XXXXXXXXXX или None."""
    if not isinstance(value, str):
        return None

    text = value.strip()
    if not text:
        return None

    has_plus = text.startswith("+")
    if has_plus:
        text = text[1:]
        if not text.startswith("7"):
            return None

    digits = []
    for character in text:
        if "0" <= character <= "9":
            digits.append(character)
        elif character not in " -()":
            return None

    number = "".join(digits)
    if len(number) == 11 and number[0] in "78":
        if has_plus and number[0] != "7":
            return None
        return "+7" + number[-10:]

    if not has_plus and len(number) == 10 and number[0] == "9":
        return "+7" + number

    return None
