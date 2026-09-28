"""Нормализация российских телефонных номеров к виду +7XXXXXXXXXX (см. TASK.md)."""

_DIGITS = frozenset("0123456789")  # только ASCII-цифры (правило 3)
_SEPARATORS = frozenset(" -()")  # допустимые разделители (правило 2)


def normalize_phone(value):
    """Вернуть номер в виде '+7XXXXXXXXXX' или None, если распознать нельзя.

    >>> normalize_phone("8 (918) 123-45-67")
    '+79181234567'
    >>> normalize_phone("abc") is None
    True
    """
    if not isinstance(value, str):  # правило 1
        return None

    text = value.strip(" ")
    has_plus = text.startswith("+")
    if has_plus:
        text = text[1:]
        if not text.startswith("7"):  # правило 4: «+» только сразу перед 7
            return None

    digits = []
    for char in text:
        if char in _DIGITS:
            digits.append(char)
        elif char not in _SEPARATORS:  # буквы, точки, второй «+» и т. п.
            return None
    number = "".join(digits)

    # Правило 5. При «+» номер уже начинается с 7 (проверено выше).
    if len(number) == 11 and number[0] in "78":
        return "+7" + number[1:]
    if len(number) == 10 and number[0] == "9":
        return "+7" + number
    return None
