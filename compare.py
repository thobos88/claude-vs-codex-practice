"""Прогон обеих реализаций normalize_phone на одном общем наборе входов.

Запуск из корня репозитория: python3 compare.py
Код возврата 0 — все найденные реализации совпали с ожидаемым, 1 — есть расхождения.
Набор кейсов составлен по правилам TASK.md до написания реализаций.
"""

import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent
OK = "+79181234567"

# (вход, ожидаемый результат, какое правило TASK.md проверяется)
CASES = [
    ("8 (918) 123-45-67", OK, "пример"),
    ("+7 918 1234567", OK, "пример"),
    ("9181234567", OK, "пример"),
    ("7-918-123-45-67", OK, "пример"),
    ("  +7 (918) 123-45-67  ", OK, "пример, пробелы по краям"),
    ("", None, "пример"),
    ("abc", None, "пример"),
    ("12345", None, "пример"),
    ("+8 918 123-45-67", None, "пример, правило 4"),
    (None, None, "пример, правило 1"),
    ("89181234567", OK, "правило 5: 11 цифр с 8"),
    ("79181234567", OK, "правило 5: 11 цифр с 7"),
    ("+79181234567", OK, "правило 4"),
    ("+7(918)123-45-67", OK, "правило 2: скобки без пробелов"),
    ("8 118 123-45-67", "+71181234567", "правило 5: 11 цифр с 8, не мобильный"),
    ("1181234567", None, "правило 5: 10 цифр не с 9"),
    ("99181234567", None, "правило 5: 11 цифр с 9"),
    ("8 918 123 45 6", None, "правило 5: 10 цифр с 8"),
    ("8 918 123 45 678", None, "правило 5: 12 цифр"),
    ("+9181234567", None, "правило 4: + не перед 7"),
    ("++7 918 123 45 67", None, "правило 4: два +"),
    ("8 918 123 45 67+", None, "правило 4: + не первым"),
    ("918.123.45.67", None, "правило 2: точка"),
    ("8 918 123 45 67 доб. 1", None, "правило 2: буквы"),
    ("8/918/123/45/67", None, "правило 2: слэш"),
    ("#89181234567", None, "правило 2: решётка"),
    ("８９１８１２３４５６７", None, "правило 3: полноширинные цифры"),
    ("٨٩١٨١٢٣٤٥٦٧", None, "правило 3: арабско-индийские цифры"),
    ("+", None, "правило 5: нет цифр"),
    ("( ) -", None, "правило 5: только разделители"),
    (89181234567, None, "правило 1: int"),
    (b"89181234567", None, "правило 1: bytes"),
    (["89181234567"], None, "правило 1: список"),
]


def load(folder):
    path = ROOT / folder / "phone.py"
    if not path.exists():
        return None
    spec = importlib.util.spec_from_file_location(f"{folder}_phone", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.normalize_phone


def main():
    failed = 0
    for folder in ("claude", "codex"):
        func = load(folder)
        if func is None:
            print(f"{folder}: реализации нет ({folder}/phone.py не найден) — пропуск")
            continue
        passed = 0
        for value, expected, rule in CASES:
            try:
                got = func(value)
            except Exception as exc:  # правило: исключения наружу не выбрасывать
                got = f"исключение {type(exc).__name__}"
            if got == expected:
                passed += 1
            else:
                failed += 1
                print(f"  {folder}: {value!r} → {got!r}, ожидалось {expected!r} ({rule})")
        print(f"{folder}: {passed}/{len(CASES)} кейсов совпали")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
