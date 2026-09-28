"""Тесты normalize_phone. Все номера вымышленные."""

import unittest

from phone import normalize_phone

OK = "+79181234567"


class ExamplesFromTask(unittest.TestCase):
    """Все примеры из таблицы TASK.md."""

    def test_examples(self):
        cases = [
            ("8 (918) 123-45-67", OK),
            ("+7 918 1234567", OK),
            ("9181234567", OK),
            ("7-918-123-45-67", OK),
            ("  +7 (918) 123-45-67  ", OK),
            ("", None),
            ("abc", None),
            ("12345", None),
            ("+8 918 123-45-67", None),
            (None, None),
        ]
        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(normalize_phone(value), expected)


class Rule1InputType(unittest.TestCase):
    def test_non_string_returns_none(self):
        for value in (89181234567, 9181234567.0, b"89181234567", ["89181234567"], True):
            with self.subTest(value=value):
                self.assertIsNone(normalize_phone(value))


class Rule2Separators(unittest.TestCase):
    def test_allowed_separators(self):
        for value in ("+7(918)123-45-67", "8 918 123 45 67", "8-918-123-45-67", "(918) 123 45 67"):
            with self.subTest(value=value):
                self.assertEqual(normalize_phone(value), OK)

    def test_other_symbols_rejected(self):
        for value in ("918.123.45.67", "8/918/123/45/67", "#89181234567", "8 918 123 45 67 доб. 1"):
            with self.subTest(value=value):
                self.assertIsNone(normalize_phone(value))


class Rule3AsciiDigits(unittest.TestCase):
    def test_non_ascii_digits_rejected(self):
        fullwidth = "８９１８１２３４５６７"
        arabic_indic = "٨٩١٨١٢٣٤٥٦٧"
        for value in (fullwidth, arabic_indic):
            with self.subTest(value=value):
                self.assertIsNone(normalize_phone(value))


class Rule4Plus(unittest.TestCase):
    def test_plus_before_seven(self):
        self.assertEqual(normalize_phone("+79181234567"), OK)

    def test_bad_plus_rejected(self):
        for value in ("+9181234567", "++7 918 123 45 67", "8 918 123 45 67+", "+", "+7 918 123 45 6"):
            with self.subTest(value=value):
                self.assertIsNone(normalize_phone(value))


class Rule5Length(unittest.TestCase):
    def test_eleven_digits_with_8_or_7(self):
        self.assertEqual(normalize_phone("89181234567"), OK)
        self.assertEqual(normalize_phone("79181234567"), OK)
        self.assertEqual(normalize_phone("8 118 123-45-67"), "+71181234567")

    def test_wrong_length_or_prefix_rejected(self):
        for value in ("1181234567", "99181234567", "8 918 123 45 6", "8 918 123 45 678", "( ) -"):
            with self.subTest(value=value):
                self.assertIsNone(normalize_phone(value))


if __name__ == "__main__":
    unittest.main()
