import unittest

from phone import normalize_phone


class NormalizePhoneTests(unittest.TestCase):
    def test_examples(self):
        cases = {
            "8 (918) 123-45-67": "+79181234567",
            "+7 918 1234567": "+79181234567",
            "9181234567": "+79181234567",
            "7-918-123-45-67": "+79181234567",
            "  +7 (918) 123-45-67  ": "+79181234567",
            "": None,
            "abc": None,
            "12345": None,
            "+8 918 123-45-67": None,
            None: None,
        }

        for value, expected in cases.items():
            with self.subTest(value=value):
                self.assertEqual(normalize_phone(value), expected)

    def test_non_string_values(self):
        for value in (9181234567, ["9181234567"], b"9181234567"):
            with self.subTest(value=value):
                self.assertIsNone(normalize_phone(value))

    def test_ascii_digits_only(self):
        self.assertIsNone(normalize_phone("８ (９１８) １２３-４５-６７"))

    def test_allowed_separators(self):
        self.assertEqual(normalize_phone("8(918) 123-45-67"), "+79181234567")

    def test_disallowed_symbols(self):
        for value in (
            "8.918.123.45.67",
            "8/918/123/45/67",
            "8#9181234567",
            "8a9181234567",
            "8\t9181234567",
        ):
            with self.subTest(value=value):
                self.assertIsNone(normalize_phone(value))

    def test_plus_sign_position_and_count(self):
        for value in (
            "++79181234567",
            "7+9181234567",
            " + 79181234567",
            "+79181234567+",
        ):
            with self.subTest(value=value):
                self.assertIsNone(normalize_phone(value))

    def test_required_prefixes_and_lengths(self):
        for value in (
            "8918123456",
            "891812345678",
            "69181234567",
            "7918123456",
            "791812345678",
            "8181234567",
            "7181234567",
            "1181234567",
            "+7918123456",
            "+791812345678",
        ):
            with self.subTest(value=value):
                self.assertIsNone(normalize_phone(value))

    def test_ten_digits_must_start_with_nine(self):
        self.assertIsNone(normalize_phone("8181234567"))


if __name__ == "__main__":
    unittest.main()
